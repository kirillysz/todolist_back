from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task.task import TaskCreate

from app.db.session import get_db
from app.core.auth_key import get_current_user
from app.crud.task.task_crud import TaskCRUD

router = APIRouter()

@router.get("/{task_id}")
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = await TaskCRUD.get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if not task:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@routet.get("/")
async def get_all_tasks(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tasks = await TaskCRUD.get_tasks_by_user(
        db=db,
        user_id=current_user.id
    )

    if not tasks:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Tasks not found"
        )

    return tasks

@router.post("/create", status_code=HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_task = await TaskCRUD.create_task(
        db=db,
        task_data=task,
        user_id=current_user.id
    )

    if not new_task:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Error creating task"
        )

    return new_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = await TaskCRUD.delete_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"detail": "Task deleted successfully"}

@router.put("/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_task = await TaskCRUD.update_task(
        db=db,
        task_id=task_id,
        task_data=task_data,
        user_id=current_user.id
    )

    if not updated_task:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task
