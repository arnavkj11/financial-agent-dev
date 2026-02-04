# Financial Advisor Agent (Backend)

An intelligent backend for a Financial AI Agent capable of processing bank statements, understanding financial data, and providing actionable insights through a conversational interface.

## 🚀 Features

*   **Smart Ingestion**: Upload PDF bank statements and automatically extract transaction data using GPT-4o vision/text capabilities.
*   **Conversational Interface**: Chat with your financial data using natural language.
*   **Hybrid Intelligence**: Uses **LangGraph** to route queries between:
    *   **SQL Database**: For precise aggregations (Sum, Count, Average) and budget tracking.
    *   **Vector Database (RAG)**: For semantic searches (e.g., "How much did I spend at coffee shops?").
*   **Financial Diagnostics**: Automatically detects high-frequency spending, potential subscriptions, and large expenses.
*   **Dashboard API**: Provides aggregated statistics and spending trends for frontend visualization.
*   **Budget Management**: Set and track budgets per category.

## 🛠️ Tech Stack

*   **Language**: Python 3.10+
*   **Framework**: FastAPI
*   **AI/LLM**: OpenAI GPT-4o
*   **Orchestration**: LangGraph, LangChain
*   **Database**:
    *   **SQL**: SQLite (via SQLAlchemy) for relational data.
    *   **Vector**: ChromaDB for semantic embeddings.
*   **Processing**: Background tasks for PDF ingestion.

## 📂 Project Structure

*   `app/api/v1`: API Route definitions.
    *   `auth.py`: Authentication endpoints (JWT).
    *   `ingestion.py`: Document upload and processing.
    *   `dashboard.py`: Statistical endpoints for UI dashboards.
    *   `budgets.py`: Budget CRUD and status checks.
    *   `chat.py`: Main entry point for the AI Agent.
*   `app/services`: Core logic.
    *   `agent.py`: LangGraph state machine configuration.
    *   `tools.py`: Custom tools available to the agent (SQL, Vector Search, Diagnostics).
    *   `pdf.py`: PDF parsing logic.
    *   `extraction.py`: LLM-based data cleaning and extraction.
*   `app/core`: Configuration, Database connection, and Security.

## ⚡ Setup Instructions

1.  **Clone the repository**
    ```bash
    git clone <repo-url>
    cd financial-agent-dev
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=sk-proj-....
    SECRET_KEY=your_secret_key_here
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

4.  **Initialize Database**
    Run the initialization script to create tables:
    ```bash
    python -m app.init_db
    ```

5.  **Run the Server**
    ```bash
    uvicorn app.main:app --reload
    ```
    Access Swagger Documentation at: `http://127.0.0.1:8000/docs`

## 📡 API Documentation

### Authentication
*   **Signup**: `POST /api/v1/auth/signup`
    *   Body: `{ "email": "user@example.com", "password": "...", "full_name": "..." }`
*   **Login**: `POST /api/v1/auth/login`
    *   Body: `{ "username": "user@example.com", "password": "..." }`
    *   Returns: `access_token` (Bearer).

### Ingestion
*   **Upload PDF**: `POST /api/v1/ingestion/ingest`
    *   Headers: `Authorization: Bearer <token>`
    *   Body: `file` (Multipart/Form-Data PDF).
    *   Note: Processing happens in the background.

### Dashboard
*   **Get Stats**: `GET /api/v1/dashboard/stats`
    *   Headers: `Authorization: Bearer <token>`
    *   Parameters:
        *   `time_range`: `24h`, `7d`, `30d` (default), `3m`, `6m`, `1y`, `all`.
        *   `categories`: List of categories to filter (e.g., `?categories=Food&categories=Travel`).
    *   Response: Total spent, top category, category breakdown (%), spending trend (daily/monthly).

### Budgets
*   **Create/Update Budget**: `POST /api/v1/budgets/`
    *   Body: `{ "category": "Food", "amount": 500.0 }`
*   **List Budgets**: `GET /api/v1/budgets/`
*   **Budget Status**: `GET /api/v1/budgets/status`
    *   Returns spending vs. limit comparison for all tracked categories.

### AI Chat
*   **Send Message**: `POST /api/v1/chat/message`
    *   Body: `{ "message": "How much did I spend on Uber last month?" }`
    *   Response: Natural language answer derived from data.

## 🤖 Agent Capabilities (Tools)

The agent has access to the following tools to answer user queries:

1.  **`run_sql_query`**: Executes simplified SQL queries to calculate totals, averages, and counts (e.g., "Total spent in December").
2.  **`search_vector_db`**: Performs semantic search on transaction descriptions to find vague matches (e.g., "Coffee" might match "Starbucks", "Dunkin").
3.  **`check_budget_status`**: Retrieves current budget limits and actual spending to warn about overspending.
4.  **`diagnose_spending`**: Runs a diagnostic report to identify:
    *   High-frequency merchants (Habits).
    *   Recurring payments (Subscriptions).
    *   Top 3 largest single expenses.
