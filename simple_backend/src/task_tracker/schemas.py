from pydantic import BaseModel


class SimpleTask(BaseModel):
    task_id: str
    task_content: str
