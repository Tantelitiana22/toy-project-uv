import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from toy_project.db import get_async_session
from toy_project.main import app

async_engine = create_async_engine(
    url="sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}
)



@pytest.fixture(scope="session")
def base_rout_path():
    return "/api/v1"

async def get_async_session_override():
    async with AsyncSession(async_engine) as session:
        yield session


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture(scope="function")
def app_fixture() -> FastAPI:
    asyncio.run(create_tables())
    app.dependency_overrides[get_async_session] = get_async_session_override
    yield app
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(app_fixture: FastAPI) -> TestClient:
    return TestClient(app_fixture)


@pytest_asyncio.fixture(scope="function")
async def async_client(app_fixture: FastAPI) -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app_fixture), base_url="http://test") as client:
        yield client
