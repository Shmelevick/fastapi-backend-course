import os

import httpx
from dotenv import load_dotenv
from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import (
    EnvError,
    TryLaterError,
)
from simple_backend.src.task_tracker.repo.abstract_task_repo import BaseRepo

load_dotenv()

BIN_ID = os.getenv("BIN_ID")
API_KEY = os.getenv("API_KEY")

if None in (BIN_ID, API_KEY):
    log.error("BIN_ID, API_KEY = {}, {}", BIN_ID, API_KEY)
    raise EnvError("Проверить .env")


class TaskRepoOuter(BaseRepo):
    BIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
    HEADERS = {"X-Access-Key": API_KEY, "Content-Type": "application/json"}

    # get
    async def get_all_tasks_repo(self) -> dict[str, dict]:
        async with httpx.AsyncClient() as client:
            raw_response = await client.get(self.BIN_URL, headers=self.HEADERS)
            raw_response.raise_for_status()
            json_response = raw_response.json()
            record = json_response.get("record")
            log.debug("\nResponse: {}\nRecord: {}", json_response, record)
            return record

    async def reset_full_doc_repo(self, all_tasks: dict) -> None:
        try:
            async with httpx.AsyncClient() as client:
                raw_response = await client.put(
                    self.BIN_URL, json=all_tasks, headers=self.HEADERS
                )
                raw_response.raise_for_status()
        except httpx.HTTPStatusError as e:
            log.error("Ошибка типа httpx.HTTPStatusError. Возможно, пустой json")
            raise TryLaterError from e


task_repo_outer = TaskRepoOuter()
