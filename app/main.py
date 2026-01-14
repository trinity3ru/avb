from contextlib import asynccontextmanager

import uvicorn
from database import engine
from fastapi import FastAPI
from routes.urls import router as urls_router

from . import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database tables are created via Alembic migrations
    print("DB is ready")
    yield
    await engine.dispose()
    print("DB is closed")


app = FastAPI(
    lifespan=lifespan,
    title="Shorten Url API",
    description="Test API for shortening URLs",
    version="1.0.4",
)

app.include_router(urls_router)

SERVER_HOST = config.SERVER_HOST
SERVER_PORT = config.SERVER_PORT

if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT)
