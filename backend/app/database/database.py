from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+asqlite:///C:/Users/sjodd/OneDrive/Desktop/project/pair-program-prototype/backend/database/main.db"

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(bind = engine, autoflush=False, expire_on_commit=False, class_ = AsyncSession) 

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session