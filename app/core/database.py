from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite for local dev. In prod, switch to Postgres.
DATABASE_URL = "sqlite+aiosqlite:///./financial_agent.db"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, # Needed for SQLite
    echo=True # Log SQL queries for debugging
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
