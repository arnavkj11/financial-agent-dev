from sqlalchemy import text
from app.core.database import SessionLocal
from app.core.vector import get_transaction_collection

from app.core.context import user_id_context

async def run_sql_query(query: str, user_id: int):
    """
    This tool executes a read-only SQL query against the database.
    Useful for aggregation capability (SUM, COUNT, AVG, etc.)
    """
    # Basic security check
    if "DROP" in query.upper() or "DELETE" in query.upper() or "INSERT" in query.upper():
        return "Error: Read-only access."

    if not user_id:
        return "Error: No user_id provided."

    print("Using run_sql_query tool", flush=True)
    print("User ID:", user_id, flush=True)
    
    # Simple Heuristic: If querying 'transactions', MUST filter by user_id
    if "transactions" in query.lower() and "user_id" not in query.lower():
         return "Error: Security Violation. You must filter by 'user_id' in your SQL query."

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

async def check_budget_status(user_id: int):
    """
    Checks the user's budget status.
    Calculates total spending vs budget limit for each category.
    Returns a formatted string summary.
    """
    try:
        if not user_id: return "Error: No user_id."

        print("Using check_budget_status tool", flush=True)
        print("User ID:", user_id, flush=True)
        query = """
        SELECT 
            b.category, 
            b.amount as limit_amount, 
            COALESCE(SUM(t.amount), 0) as spent
        FROM budgets b
        LEFT JOIN transactions t ON b.category = t.category AND t.user_id = b.user_id
        WHERE b.user_id = :uid
        GROUP BY b.id
        """
        
        async with SessionLocal() as session:
            result = await session.execute(text(query), {"uid": user_id})
            rows = result.fetchall()
            
            if not rows:
                return "No budgets set."
                
            report = "Budget Report:\n"
            for row in rows:
                category, limit, spent = row
                percent = (spent / limit) * 100 if limit > 0 else 0
                report += f"Category: {category} | Spent: ${spent:.2f} / ${limit:.2f} ({percent:.1f}%)\n"
            
            return report
            
    except Exception as e:
        return f"Budget Tool Error: {e}"

async def diagnose_spending(user_id: int):
    """
    Analyzes financial data to find patterns:
    1. High Frequency Merchants (The 'Latte Factor').
    2. Potential Subscriptions (Same amount > 2 times).
    3. Largest Single Expenses.
    """
    report = "--- Financial Diagnostics Report ---\n"
    print("Using diagnose_spending tool", flush=True)
    print("User ID:", user_id, flush=True)
    
    async with SessionLocal() as session:
        # 1. High Frequency
        freq_query = """
        SELECT merchant, COUNT(*) as cnt, SUM(amount) as total
        FROM transactions 
        WHERE user_id = :uid
        GROUP BY merchant 
        HAVING cnt > 4
        ORDER BY cnt DESC
        LIMIT 5
        """
        result = await session.execute(text(freq_query), {"uid": user_id})
        rows = result.fetchall()
        if rows:
            report += "\n[High Frequency Habits]\n"
            for row in rows:
                report += f"- {row.merchant}: {row.cnt} times (Total: ${row.total})\n"

        # 2. Potential Subscriptions
        sub_query = """
        SELECT merchant, amount, COUNT(*) as cnt
        FROM transactions
        WHERE user_id = :uid AND amount > 5
        GROUP BY merchant, amount
        HAVING cnt > 1
        ORDER BY cnt DESC
        LIMIT 5
        """
        result = await session.execute(text(sub_query), {"uid": user_id})
        rows = result.fetchall()
        if rows:
            report += "\n[Potential Subscriptions / Recurring]\n"
            for row in rows:
                report += f"- {row.merchant}: ${row.amount} (seen {row.cnt} times)\n"
        
        # 3. Top Spenders
        top_query = """
        SELECT merchant, amount, date, category
        FROM transactions
        WHERE user_id = :uid
        ORDER BY amount DESC
        LIMIT 3
        """
        result = await session.execute(text(top_query), {"uid": user_id})
        rows = result.fetchall()
        if rows:
            report += "\n[Largest Single Expenses]\n"
            for row in rows:
                report += f"- {row.merchant}: ${row.amount} ({row.category}) on {row.date}\n"

    return report

async def search_vector_db(query: str, user_id: int, n_results: int = 5):
    """
    This tool searches the vector database for transaction descriptions.
    Useful for finding specific merchants or categories.
    """
    try:
        if not user_id: return "Error: No user_id."

        collection = get_transaction_collection()
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id} # RLS Filter
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
