import httpx
from fastapi import HTTPException, status
from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import TaskNotFoundError, TryLaterError
from simple_backend.src.task_tracker.outer_llm import llm_service
from simple_backend.src.task_tracker.schemas import SimpleTask

# .env
BIN_ID = "69132f8043b1c97be9a6c736"
API_KEY = "$2a$10$.I90TG0hqqvbhv1tmOU3VePLR7hFWX7K71Cjnsy.on1brj04SsrE."


class TaskRepo:
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

    @classmethod
    def get_next_id(cls, all_tasks: dict[str, dict[str, str]]) -> str:
        log.debug("all_tasks: {}", all_tasks)
        try:
            next_id = max(int(k) for k in all_tasks if k.isdigit()) + 1
            log.debug("Next_id: {}", next_id)
            return str(next_id) or "1"
        except ValueError:
            log.error("Ошибка! Нет числовых значений в all_tasks!")
            return "1"

    # create
    async def add_new_task_repo(self, task_content: str):
        all_tasks = await self.get_all_tasks_repo()
        next_id = self.get_next_id(all_tasks)
        log.debug("next_id: {}, task_content: {}", next_id, task_content)

        llm_solution = await llm_service.make_request(task_content)
        all_tasks[next_id] = {
            "task_id": next_id,
            "task_content": task_content,
            "task_solution": llm_solution,
        }
        await self.reset_full_doc_repo(all_tasks)

    # update
    async def update_task_repo(self, task_id: str, new_task_content: str) -> SimpleTask:
        all_tasks = await self.get_all_tasks_repo()
        old_task_content = all_tasks.get(task_id)

        # not found
        if task_id not in all_tasks:
            log.error(
                "Task not found.\ntask_id: {}, task_content: {}, all_tasks: {}",
                task_id,
                new_task_content,
                all_tasks,
            )
            raise TaskNotFoundError

        llm_solution = await llm_service.make_request(new_task_content)

        updated_task = {
            "task_id": task_id,
            "task_content": new_task_content,
            "task_solution": llm_solution,
        }
        all_tasks[task_id] = updated_task
        await self.reset_full_doc_repo(all_tasks)

        log.info("Updated task {}: {} -> {}", task_id, old_task_content, updated_task)
        return SimpleTask(**updated_task)

    # delete
    async def delete_task_repo(self, task_id: str) -> None:
        all_tasks = await self.get_all_tasks_repo()

        print(task_id, type(task_id), all_tasks)
        print(repr(task_id))
        print(type(list(all_tasks.keys())))

        # not found
        if task_id not in all_tasks:
            log.error(
                "Task not found.\ntask_id: {}, all_tasks: {}",
                task_id,
                all_tasks,
            )
            raise TaskNotFoundError

        log.info("Сейчас удалится запись id={}: {}", task_id, all_tasks[task_id])
        del all_tasks[task_id]
        await self.reset_full_doc_repo(all_tasks)


task_repo = TaskRepo()
