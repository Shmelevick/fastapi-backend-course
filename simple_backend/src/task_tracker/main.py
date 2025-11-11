import uvicorn
from fastapi import FastAPI
from loguru import logger as log

from simple_backend.src.task_tracker.router import router

app = FastAPI()
app.include_router(router)
