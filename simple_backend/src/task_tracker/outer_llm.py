import httpx
from loguru import logger as log

# .env
API_TOKEN = "ZOXT38HqVHmWwczS0QVN_en_01-LAC_xCZjcbmZp"
ACCOUNT_ID = "98059c84d2b66b5c06a1347a81f0ca37"
MODEL = "llama-3.1-8b-instruct"


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
