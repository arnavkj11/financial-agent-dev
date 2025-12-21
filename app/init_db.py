import asyncio
import os
import shutil
from app.core.database import engine, Base
from app.models.sql import User, Document, Transaction

async def init_models():
    # 1. Reset SQL
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all) # Uncomment to drop SQL tables
        await conn.run_sync(Base.metadata.create_all)
    print("SQL Tables created successfully.")

    # 2. Reset Vector DB (Development Mode)
    # This prevents "Ghost Data" when you reset the DB but keep the embeddings
    persist_dir = os.path.join(os.getcwd(), "chroma_db")
    if os.path.exists(persist_dir):
        try:
            shutil.rmtree(persist_dir)
            print(f"Cleared existing Vector DB at: {persist_dir}")
        except Exception as e:
            print(f"Error clearing Vector DB: {e}")

if __name__ == "__main__":
    asyncio.run(init_models())
