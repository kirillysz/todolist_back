from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.auth.route import router as auth_router
from app.api.task.route import router as task_router

from app.db.init_tables import init_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await init_tables()
    yield
    # Shutdown code (if any)

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
