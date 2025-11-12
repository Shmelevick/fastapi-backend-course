from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import TaskNotFoundError
from simple_backend.src.task_tracker.repo.repository import task_repo
from simple_backend.src.task_tracker.schemas import SimpleTask


class TaskService:
    async def get_all_tasks_service(self) -> dict:
        return await task_repo.get_all_tasks_repo()

    async def add_new_task_sevice(self, task):
        await task_repo.add_new_task_repo(task)

    async def update_task_service(self, task_id, new_task_content) -> SimpleTask:
        return await task_repo.update_task_repo(task_id, new_task_content)

    async def delete_task_service(self, task_id):
        await task_repo.delete_task_repo(task_id)


task_service = TaskService()
