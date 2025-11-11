import httpx
from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import TaskNotFoundError
from simple_backend.src.task_tracker.schemas import SimpleTask

# .env
BIN_ID = "69132f8043b1c97be9a6c736"
API_KEY = "$2a$10$.I90TG0hqqvbhv1tmOU3VePLR7hFWX7K71Cjnsy.on1brj04SsrE."


class TaskRepo:
    BIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
    HEADERS = {"X-Access-Key": API_KEY, "Content-Type": "application/json"}

    # @classmethod вызывает проблемы с асинхронностью
    async def get_all_tasks_repo(self) -> dict:
        async with httpx.AsyncClient() as client:
            raw_response = await client.get(self.BIN_URL, headers=self.HEADERS)
            json_response = raw_response.json()
            record = json_response.get("record")
            log.debug("\nResponse: {}\nRecord: {}", json_response, record)
            print(type(record), record["1"])
            return record

    async def reset_full_doc_repo(self, all_tasks: dict) -> None:
        async with httpx.AsyncClient() as client:
            raw_response = await client.put(
                self.BIN_URL, json=all_tasks, headers=self.HEADERS
            )
            print(raw_response)

    def get_next_id(self, all_tasks: dict[str, str]) -> str:
        next_id = max(int(k) for k in all_tasks) + 1
        return str(next_id)

    # get
    async def get_task_by_id_repo(self, task_id: str) -> SimpleTask:
        all_tasks = await self.get_all_tasks_repo()
        task_content = all_tasks.get(task_id)

        if task_id not in all_tasks or task_content is None:
            log.error(
                "Task not found.\ntask_id: {}, task_content: {}, all_tasks: {}",
                task_id,
                task_content,
                all_tasks,
            )
            raise TaskNotFoundError

        log.debug("task id: {}, task: {}", task_id, task_content)
        return SimpleTask(task_id=task_id, task_content=task_content)

    # create
    async def add_new_task_repo(self, task: str):
        all_tasks = await self.get_all_tasks_repo()
        next_id = self.get_next_id(all_tasks)
        all_tasks[next_id] = task
        await self.reset_full_doc_repo(all_tasks)

    # update
    async def update_task_repo(self, task_id: str, new_task_content: str) -> SimpleTask:
        """Частично повторим get_task_by_id, чтобы сделать меньше внешних запросов"""
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

        all_tasks[task_id] = new_task_content
        await self.reset_full_doc_repo(all_tasks)

        updated_task = SimpleTask(task_id=task_id, task_content=new_task_content)
        log.info("Updated task {}: {} -> {}", task_id, old_task_content, updated_task)
        return updated_task

    # delete
    async def delete_task_repo(self, task_id: str) -> None:
        all_tasks = await self.get_all_tasks_repo()

        # not found
        if task_id not in all_tasks:
            log.error(
                "Task not found.\ntask_id: {}, all_tasks: {}",
                task_id,
                all_tasks,
            )
            raise TaskNotFoundError

        log.info("Удалена запись id={}: {}", task_id, all_tasks[task_id])
        del all_tasks[task_id]
        await self.reset_full_doc_repo(all_tasks)


task_repo = TaskRepo()
