from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import TaskNotFoundError
from simple_backend.src.task_tracker.repository import (
    add_new_task_repo,
    delete_task_repo,
    get_all_tasks_repo,
    get_task_by_id_repo,
    update_task_repo,
)
from simple_backend.src.task_tracker.schemas import SimpleTask


async def get_all_tasks_service() -> dict:
    return await get_all_tasks_repo()


async def get_task_by_id(task_id: str) -> SimpleTask:
    return await get_task_by_id_repo(task_id)


async def add_new_task_sevice(task):
    await add_new_task_repo(task)


async def update_task_service(task_id, new_task_content) -> SimpleTask:
    return await update_task_repo(task_id, new_task_content)


async def delete_task_service(task_id):
    await delete_task_repo(task_id)
