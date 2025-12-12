# Financial Advisor Agent (Backend)

Hello! This is my project for building a Financial AI Agent. I created this backend because I wanted to learn how to make AI that can understand bad PDF bank statements and answer questions about money.

## What it does?

Basically, this is smart backend where you can:
1. **Login/Signup**: It has secure authentication with JWT (so your data is safe).
2. **Upload PDFs**: You can upload your bank statement (PDF).
3. **Magic Processing**: A worker extracts the text and uses GPT-4o to "clean" the data. It finds the date, merchant, amount, and category.
4. **Chat with Data**: You can ask questions like *"How much I spent on coffee?"* or *"What did I buy last week?"*.

## The "Brain"

I used **LangGraph** to make the agent smart. It decides if it needs to use:
*   **SQL Database**: For math questions (Sum, Count, Average).
*   **Vector Database**: For search questions (finding specific shops or items).

It uses **RAG** (Retrieval Augmented Generation) to give the answer.

## Tech Stack

I used these tools:
*   **Python**: My favorite language.
*   **FastAPI**: For making the API endpoints.
*   **OpenAI GPT-4o**: To understand the text.
*   **LangGraph & LangChain**: To build the agent logic.
*   **SQLAlchemy & SQLite**: To save the transactions.
*   **ChromaDB**: To save embeddings for searching.

## How to Run it on your PC

If you want to try my code, follow these steps:

1.  **Clone the repo**
    ```bash
    git clone <repo-url>
    cd financial-agent-dev
    ```

2.  **Install requirements**
    Make sure you have Python installed.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Keys**
    Create a `.env` file and put your OpenAI Key:
    ```
    OPENAI_API_KEY=sk-proj-....
    SECRET_KEY=mysecretkey
    ```

4.  **Init Database**
    Run this script to make the tables:
    ```bash
    python app/init_db.py
    ```

5.  **Start Server**
    ```bash
    uvicorn app.main:app --reload
    ```
    Then go to `http://127.0.0.1:8000/docs` to see the Swagger UI.

## Thank You!
