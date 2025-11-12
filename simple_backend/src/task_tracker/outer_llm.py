import os

import httpx
from dotenv import load_dotenv
from loguru import logger as log

from simple_backend.src.task_tracker.exceptions import EnvError

load_dotenv()

# .env
API_TOKEN = str(os.getenv("API_TOKEN"))
ACCOUNT_ID = str(os.getenv("ACCOUNT_ID"))
MODEL = str(os.getenv("MODEL"))

if None in (API_TOKEN, ACCOUNT_ID, MODEL):
    log.error("API_TOKEN, ACCOUNT_ID, MODEL = {}, {}, {}", API_TOKEN, ACCOUNT_ID, MODEL)
    raise EnvError("Проверить .env")


class LLMService:
    HEADERS = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/{MODEL}"

    async def make_request(self, request_text: str) -> str:
        async with httpx.AsyncClient() as client:
            raw_response = await client.post(
                self.URL,
                headers=self.HEADERS,
                json={
                    "prompt": "Уложись в 867 символов. Объясни, как мне " + request_text
                },
            )
            raw_response.raise_for_status()
            llm_response = raw_response.json()
            log.debug("Ответ LLM: {}", llm_response)
            llm_solution = llm_response["result"]["response"]
            return llm_solution


llm_service = LLMService()
