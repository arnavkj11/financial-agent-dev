import asyncio
from app.core.database import engine, Base
from app.models.sql import User, Document, Transaction

async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) #uncomment to reset DB
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_models())
