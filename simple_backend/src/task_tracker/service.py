import os

from dotenv import load_dotenv
from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import (
    EnvError,
)  # noqa: F401
from simple_backend.src.task_tracker.schemas import SimpleTask

load_dotenv()

REPO = os.getenv("REPO")
match REPO:
    case "LOCAL":
        log.info("REPO = {}", REPO)
        from simple_backend.src.task_tracker.repo.task_repo_local_json import (
            task_repo_local as task_repo,
        )  # noqa: F401
    case "OUTER":
        log.info("REPO = {}", REPO)
        from simple_backend.src.task_tracker.repo.task_repo_outer_json import (
            task_repo_outer as task_repo,
        )  # noqa: F401
    case _:
        log.error("REPO = {}", REPO)
        raise EnvError("Проверить .env")


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
