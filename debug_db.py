import asyncio
from sqlalchemy import text
from app.core.database import SessionLocal

async def check_netflix():
    async with SessionLocal() as session:
        # Check specific merchant
        result = await session.execute(text("SELECT * FROM transactions WHERE merchant LIKE '%Netflix%'"))
        rows = result.fetchall()
        print(f"--- Netflix Transactions Found: {len(rows)} ---")
        for row in rows:
            print(row)

        # Check all counts
        result_count = await session.execute(text("SELECT count(*) FROM transactions"))
        print(f"\nTotal Transactions: {result_count.scalar()}")

        # Check Documents
        result_docs = await session.execute(text("SELECT * FROM documents"))
        print("\n--- Documents ---")
        for doc in result_docs.fetchall():
            print(doc)

if __name__ == "__main__":
    asyncio.run(check_netflix())
