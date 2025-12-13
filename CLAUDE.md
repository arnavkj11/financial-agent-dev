# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Financial AI Agent backend that processes PDF bank statements and enables natural language queries about financial transactions. The system uses a LangGraph-based agent that intelligently routes queries between SQL (for aggregations) and vector database (for semantic search).

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database tables
python app/init_db.py

# Start development server
uvicorn app.main:app --reload
```

### Running the Server
```bash
# Standard startup
uvicorn app.main:app --reload

# Direct execution
python app/main.py
```

API documentation available at: `http://127.0.0.1:8000/docs`

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=sk-proj-...
SECRET_KEY=mysecretkey
```

## Architecture

### Agent Design (LangGraph)
The core intelligence lives in `app/services/agent.py`. The agent uses a state graph pattern:

1. **Agent Node**: Analyzes user query and decides which tool to invoke
2. **Tool Node**: Executes either SQL query or vector search
3. **Conditional Routing**: Loops back to agent if tool was called, otherwise ends

The agent has access to two tools:
- `query_sql_tool`: For aggregations (SUM, COUNT, AVG) on structured transaction data
- `vector_search_tool`: For semantic search (finding merchants/categories by meaning)

### Data Flow
```
PDF Upload → Text Extraction → LLM Structuring → Dual Storage (SQL + Vector) → Agent Queries
```

1. **Ingestion** (`app/api/v1/endpoints/ingestion.py`):
   - Receives PDF upload via `/api/v1/documents/ingest`
   - Saves file and triggers background processing task

2. **Processing** (`app/services/pdf.py`):
   - Extracts text using pypdf
   - Calls GPT-4o to structure data via `app/services/extraction.py`
   - Stores in both SQLite (structured) and ChromaDB (embeddings)

3. **Querying** (`app/api/v1/endpoints/chat.py`):
   - User sends natural language query to `/api/v1/chat/message`
   - LangGraph agent decides tool routing
   - Returns synthesized answer

### Database Architecture

**SQL Database** (`app/models/sql.py`):
- `users`: Authentication (email, hashed_password)
- `documents`: Uploaded PDFs and processing status
- `transactions`: Extracted financial data (date, merchant, amount, category)

**Vector Database** (`app/core/vector.py`):
- ChromaDB collection: `financial_transactions`
- Embeddings via OpenAI `text-embedding-3-small`
- Indexed documents combine merchant, category, date, and amount for semantic search

### Key Components

**app/services/extraction.py**: Uses LangChain's `with_structured_output` to guarantee Pydantic-validated JSON from GPT-4o. Extracts and categorizes transactions from unstructured text.

**app/services/tools.py**: Implements the two agent tools:
- SQL tool includes basic security checks (no DROP/DELETE/INSERT)
- Vector tool returns top-N semantic matches

**app/core/config.py**: Centralized settings loaded from environment variables

**app/core/security.py**: JWT-based authentication (referenced but not shown in analysis)

### Authentication
JWT-based auth implemented in `app/api/v1/endpoints/auth.py`. Protected endpoints require `get_current_user` dependency from `app/api/deps.py`.

## Important Notes

### Database Initialization
Always run `python app/init_db.py` after cloning or when adding new models. The script creates tables based on SQLAlchemy models.

### Async Pattern
The codebase uses async/await throughout:
- FastAPI endpoints are async
- Database sessions use AsyncSession (aiosqlite)
- LangGraph agent invocation uses `ainvoke()`

### LLM Integration
- Main model: GPT-4o for both extraction and agent reasoning
- Embedding model: text-embedding-3-small for vector store
- LangChain's structured output ensures type-safe LLM responses

### Background Processing
Document processing happens asynchronously via FastAPI's BackgroundTasks. The upload endpoint returns immediately while extraction/indexing runs in the background. Check `documents.status` field for processing state.

### Tool Routing Logic
The agent's system prompt (in `agent.py`) instructs it to:
1. Use SQL for mathematical operations (totals, averages, counts)
2. Use vector search for finding specific merchants or semantic queries
3. The schema is injected into the system message for SQL query generation
