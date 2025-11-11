from fastapi import APIRouter, Body, HTTPException, status
from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import TaskNotFoundError
from simple_backend.src.task_tracker.service import (
    add_new_task_sevice,
    delete_task_service,
    get_all_tasks_service,
    update_task_service,
)

router = APIRouter()


@router.get("/tasks")
async def get_tasks():
    try:
        return await get_all_tasks_service()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error on server"
        ) from e


@router.post("/tasks")
async def create_task(task):
    try:
        await add_new_task_sevice(task)
        return {
            "message": "Заметка успешно создана!",
            "status": status.HTTP_201_CREATED,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error on server"
        ) from e


@router.put("/tasks/{task_id}")
async def update_task(task_id: str, task_content: str = Body(...)):
    try:
        updated_task = await update_task_service(task_id, task_content)
        return {
            "message": f"Заметка {task_id} успешно обновлена! Теперь это: {updated_task}",
            "status": status.HTTP_200_OK,
        }
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        ) from e


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        await delete_task_service(task_id)
        return {"message": f"Заметка {task_id} удалена", "status": status.HTTP_200_OK}
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        ) from e
