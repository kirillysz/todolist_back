from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from contextlib import asynccontextmanager

from app.api.auth.route import router as auth_router
from app.api.task.route import router as task_router

from app.db.init_tables import init_tables

from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tables()
    yield

origins = settings.ORIGINS.split(",")

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "DELETE", "PUT"],
    allow_headers=["Content-Type"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
