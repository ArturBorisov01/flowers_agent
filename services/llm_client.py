# services/llm_client.py
import httpx
from typing import Any, Optional

from langchain_openrouter import ChatOpenRouter
from core.config import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

llm = ChatOpenRouter(
    model=settings.model_name,
    temperature=0,
    max_tokens=1024,
    max_retries=2,
)


async def chat_completion(
    messages: list[dict],
    tools: Optional[list[Any]] = None,
    json_mode: bool = False,
) -> dict:
    """Основной вызов модели с полной историей сообщений (сырой HTTP, без LangChain)."""
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.model_name,
        "messages": messages,
    }
    if tools:
        payload["tools"] = tools
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            message_data = data["choices"][0]["message"]

            if message_data.get("tool_calls"):
                return {"status": "tool_call", "calls": message_data["tool_calls"]}

            return {"status": "text", "content": message_data.get("content", "")}

        except Exception as e:
            return {"status": "error", "content": f"Ошибка при запросе к OpenRouter: {str(e)}"}


async def process_message(prompt: str) -> dict:
    """Обёртка для простого одноразового запроса — используется в /test_connection_model."""
    return await chat_completion([{"role": "user", "content": prompt}])