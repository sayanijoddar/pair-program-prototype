# database/database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
import os

# Absolute path with forward slashes
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "main.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH.replace(os.sep, '/')}"

# Create engine directly - NO lazy init
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False later
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
