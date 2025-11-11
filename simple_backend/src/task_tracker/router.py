from fastapi import APIRouter

router = APIRouter()


@router.get("/tasks")
def get_tasks():
    pass


@router.post("/tasks")
def create_task(task):
    pass


@router.put("/tasks/{task_id}")
def update_task(task_id: int):
    pass


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    pass
