from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.task import Task
from app.schemas.task.task import TaskCreate

class TaskCRUD:
    @staticmethod
    async def get_tasks_by_user(
        db: AsyncSession,
        user_id: int
    ) -> list[Task]:
        tasks = await db.execute(
            select(Task).where(
                Task.user_id == user_id
            )
        )

        return tasks.scalars().all()

    @staticmethod
    async def get_task_by_id(
        db: AsyncSession,
        task_id: int,
        user_id: int
    ) -> Task | None:
        task = await db.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
        )
    
        return task.scalar_one_or_none()

    @staticmethod
    async def create_task(
        db: AsyncSession,
        task_data: TaskCreate,
        user_id: int
    ) -> Task:
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id
        )

        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)

        return new_task

    @staticmethod
    async def delete_task(
        db: AsyncSession,
        task_id: int,
        user_id: int
    ) -> bool:
        task = await TaskCRUD.get_task_by_id(db, task_id, user_id)

        if not task:
            return False

        await db.delete(task)
        await db.commit()

        return True
    
    @staticmethod
    async def update_task(
        db: AsyncSession,
        task_id: int,
        task_data: TaskCreate,
        user_id: int
    ) -> Task | None:
        task = await TaskCRUD.get_task_by_id(db, task_id, user_id)

        if not task:
            return None

        task.title = task_data.title
        task.description = task_data.description
        task.completed = task_data.completed

        db.add(task)
        await db.commit()
        await db.refresh(task)

        return task