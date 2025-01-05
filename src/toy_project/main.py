from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from toy_project.db import async_engine
from toy_project.services.product import router


@asynccontextmanager
async def life_span(_: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await async_engine.dispose()


app = FastAPI(title="Product Management", lifespan=life_span)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
