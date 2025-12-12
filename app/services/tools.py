from sqlalchemy import text
from app.core.database import SessionLocal
from app.core.vector import get_transaction_collection

async def run_sql_query(query: str):
    """
    This tool executes a read-only SQL query against the database.
    Useful for aggregation capability (SUM, COUNT, AVG, etc.)
    """
    # Basic security check
    if "DROP" in query.upper() or "DELETE" in query.upper() or "INSERT" in query.upper():
        return "Error: Read-only access."

    try:
        async with SessionLocal() as session:
            result = await session.execute(text(query))
            rows = result.fetchall()
            # Convert to list of dicts for LLM readability
            if not rows:
                return "No results found."
            return [dict(row._mapping) for row in rows]
    except Exception as e:
        return f"Database Error: {e}"

def search_vector_db(query: str, n_results: int = 5):
    """
    This tool searches the vector database for transaction descriptions.
    Useful for finding specific merchants or categories.
    """
    try:
        collection = get_transaction_collection()
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        # Flatten results
        return results["documents"][0]
    except Exception as e:
        return f"Vector Store Error: {e}"

def get_db_schema():
    """
    This tool returns the schema info for the LLM to write SQL.
    """
    return """
    Table: transactions
    Columns:
    - date (Date)
    - merchant (String)
    - amount (Float)
    - currency (String)
    - category (String)
    """
