import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)


async def get_async_session() -> AsyncSession:
    async with AsyncSession(async_engine) as session:
        yield session
