# Technical Deep Dive: Financial Advisor Agent with RAG

## 1. Project Overview
This project is an **Autonomous Financial Agent** designed to ingest unstructured PDF bank statements, process them into structured data, and provide an interactive chat interface for financial analysis.
It leverages **Retrieval-Augmented Generation (RAG)** to ground Large Language Model (LLM) responses in the user's actual financial data.

## 2. Technical Architecture
The backend is built using **Python** and **FastAPI**, chosen for their asynchronous capabilities and strong integration with the AI ecosystem.

### Core Stack
*   **API Framework**: FastAPI (Async/Await)
*   **LLM Orchestration**: LangGraph (Stateful Multi-step Agents) & LangChain
*   **Intelligence**: OpenAI GPT-4o
*   **Database (Hybrid Memory)**:
    *   **Structured**: SQLite (via SQLAlchemy Async) for quantitative analysis (SUM, AVG).
    *   **Unstructured**: ChromaDB (Vector Store) for semantic search.
*   **Security**: OAuth2 with JWT (JSON Web Tokens) & Passlib/Bcrypt.

## 3. Implementation Journey (How I Built It)

I broke the development into 6 logical phases to ensure modularity and testability.

### Phase 1: Infrastructure & Architecture
I started by defining a clean folder structure adhering to "Clean Clean Architecture" principles:
*   `app/api`: Routing and Controllers.
*   `app/services`: Business Logic (PDF parsing, Agent logic).
*   `app/core`: Configuration and Security.
*   `app/models`: Database Schemas.

### Phase 2: Core Skeleton
I initialized the FastAPI app and configured the environment (`pydantic-settings`). I established the async database connection using `aiosqlite` and `SQLAlchemy`.

### Phase 3: The Data Pipeline (ETL)
**Challenge**: PDF bank statements are messy unstructured text.
**Solution**: I built a robust ETL (Extract, Transform, Load) pipeline in `app/services/pdf.py`.
1.  **Extract**: `pypdf` reads the raw text stream.
2.  **Transform (Intelligence)**: I pass the raw text to **GPT-4o** with a Pydantic Model (`CleanData`). This forces the LLM to output precise JSON (Merchant, Date, Amount, Category).
3.  **Load**: The background worker saves the data to SQL.

### Phase 4: Data Persistence (Hybrid Memory)
To enable the agent to answer *any* question, I needed two types of storage:
1.  **SQL Database**: For questions like "Total spend on Food". (LLM generates SQL queries).
2.  **Vector Store**: For questions like "Did I buy any coffee?". (LLM performs semantic similarity search).
**Implementation**: I integrated `ChromaDB`. During the ingestion loop, I simultaneously save the transaction to SQL and generate an embedding (vector) of the description `"{Merchant} ({Category})"`, ensuring both databases are always in sync.

### Phase 5: The Agentic Brain (LangGraph)
**Why LangGraph?**: Standard RAG is linear. I needed an Agent that could *reason* and loop.
**Logic**:
1.  **Router**: The Agent receives a user message.
2.  **Tool Selection**: It decides: "Is this a math problem?" (Call `query_sql_tool`) or "Is this a search problem?" (Call `vector_search_tool`).
3.  **Execution**: It runs the tool, gets the data, and generates a natural language response.
This logic is encapsulated in `app/services/agent.py`.

### Phase 6: Security (Authentication)
I implemented industry-standard security manually (to learn the details):
1.  **Hashing**: Passwords are hashed using `bcrypt` (via `passlib`).
2.  **Tokens**: On login, I issue a **JWT (Bearer Token)** signed with a `SECRET_KEY`.
3.  **Dependency Injection**: I created a `get_current_user` dependency. This "Bouncer" function sits before every protected endpoint (`/chat`, `/ingest`), verifying the token and decoding the User ID.

## 4. Key Code Components to Review

### `app/services/agent.py` (The Brain)
This file defines the **State Graph**. It uses `Annotated[list, add_messages]` to preserve conversation history. It binds the SQL and Vector tools to the LLM, giving it "hands" to interact with the database.

### `app/services/pdf.py` (The Worker)
This is the workhorse. It handles the asynchronous background task. I heavily optimized this to perform the SQL insertion and Vector indexing in a single pass to ensure data consistency (fixing an early bug where IDs were missing).

### `app/services/tools.py` (The Tools)
This contains the specific logic the agent uses. 
*   `run_sql_query`: Executes read-only SQL for aggregation.
*   `search_vector_db`: Queries ChromaDB for semantic matches.

## 5. Conclusion
This project demonstrates a complete end-to-end AI application. It moves beyond simple "chatbot wrappers" by integrating deep backend engineering (Async SQL, queue management, security) with modern Agentic design patterns (Tool use, RAG, Hybrid Search).
