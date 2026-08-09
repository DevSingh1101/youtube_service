from fastapi import FastAPI, Depends
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from controller import user_router
from core import DatabaseManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_manager = DatabaseManager()
    SQLModel.metadata.create_all(database_manager.engine)
    yield


app = FastAPI(title="youtube-automation-service", lifespan=lifespan)

@app.get("/")
def home():
    return {
        "service": "youtube-automation-service",
        "version": "v1",
    }


@app.get("/health")
def health():
    return {
        "service": "youtube-automation-service",
        "status": "ok",
    }

app.include_router(user_router)