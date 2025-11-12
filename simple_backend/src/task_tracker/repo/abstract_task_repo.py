from abc import ABC, abstractmethod

from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import TaskNotFoundError
from simple_backend.src.task_tracker.outer_llm import llm_service
from simple_backend.src.task_tracker.schemas import SimpleTask


class BaseRepo(ABC):
    # реализация на уровне наследника
    @abstractmethod
    async def get_all_tasks_repo(self) -> dict:
        pass

    @abstractmethod
    async def reset_full_doc_repo(self, all_tasks) -> None:
        pass

    # общая функциональность
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
        all_tasks: dict = await self.get_all_tasks_repo()
        next_id = self.get_next_id(all_tasks)
        log.debug("next_id: {}, task_content: {}", next_id, task_content)

        llm_solution = await llm_service.make_request(task_content)
        all_tasks[next_id] = {
            "task_id": next_id,
            "task_content": task_content,
            "task_solution": llm_solution,
        }
        log.debug("task: {}", all_tasks[next_id])
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
