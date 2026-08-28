# services/llm_client.py
import os
import httpx
from typing import Any, Optional


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


async def chat_completion(messages: list[dict], tools: Optional[list[Any]] = None) -> dict:
    """Основной вызов модели с полной историей сообщений."""
    # print("DEBUG key:", os.getenv("OPENROUTER_API_KEY"))
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": os.getenv("MODEL_NAME"),
        "messages": messages,
        "response_format": {"type": "json_object"}, # если модель поддерживает
    }
    if tools:
        payload["tools"] = tools

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