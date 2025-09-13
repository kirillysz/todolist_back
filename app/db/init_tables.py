from app.db.models.user import User
from app.db.models.task import Task

from app.db.base import Base
from app.db.session import engine

async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)