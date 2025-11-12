import json
import os
from typing import cast

import aiofiles
from dotenv import load_dotenv
from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import EnvError, TaskNotFoundError
from simple_backend.src.task_tracker.outer_llm import llm_service
from simple_backend.src.task_tracker.repo.abstract_task_repo import BaseRepo
from simple_backend.src.task_tracker.schemas import SimpleTask

# .env
load_dotenv()

FILE_PATH = str(os.getenv("FILE_PATH"))

if FILE_PATH is None:
    log.error("FILE_PATH = {}", FILE_PATH)
    raise EnvError("Проверить .env")


class TaskRepoLocal(BaseRepo):
    async def create_file(self) -> None:
        try:
            async with aiofiles.open(FILE_PATH, "w", encoding="utf-8") as f:
                await f.write(json.dumps({}))
        except Exception as e:
            log.error("Ошибка при создании json файла: {}", e)
            raise e

    async def get_all_tasks_repo(self) -> dict:
        # create empty if not exists
        if not os.path.exists(FILE_PATH):
            await self.create_file()

        try:
            async with aiofiles.open(FILE_PATH, encoding="utf-8") as f:
                data = json.loads(await f.read())
                return data
        except Exception as e:
            log.error("Ошибка в чтении json файла: {}", e)
            raise e

    async def reset_full_doc_repo(self, all_tasks) -> None:
        # create empty if not exists
        if not os.path.exists(FILE_PATH):
            await self.create_file()

        try:
            async with aiofiles.open(FILE_PATH, "w", encoding="utf-8") as f:
                await f.write(json.dumps(all_tasks))
        except Exception as e:
            log.error("Ошибка в записи в json файл: {}", e)
            raise e


task_repo_local = TaskRepoLocal()
