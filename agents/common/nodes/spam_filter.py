# agents/common/nodes/spam_filter.py
import json
from langchain_core.messages import AIMessage
from agents.state import AgentState
from services.llm_client import chat_completion

MAX_MESSAGE_LENGTH = 1000

CLASSIFICATION_PROMPT = """
Проанализируй сообщение клиента и определи два признака.

Сообщение:
"{message}"

Ответь СТРОГО в формате JSON, без пояснений и текста вокруг:
{{
    "is_aggressive": true/false,
    "is_commercial_offer": true/false
}}

Критерии:
- is_aggressive: сообщение содержит оскорбления, угрозы, грубость, нецензурную лексику
- is_commercial_offer: сообщение является рекламой, спам-рассылкой, предложением услуг от третьих лиц (не вопрос клиента о товаре/услуге компании)
"""


async def check_spam(state: AgentState) -> dict:
    last_message = state["messages"][-1]
    message = last_message.content.strip()

    if len(message) == 0 or len(message) > MAX_MESSAGE_LENGTH:
        return {"is_spam": True, "spam_reason": "invalid_length"}

    try:
        classification = await _classify_message(message)
    except Exception:
        # Если что-то пошло не так — не блокируем клиента, пропускаем дальше
        return {"is_spam": False, "spam_reason": None}

    if classification.get("is_aggressive"):
        return {"is_spam": True, "spam_reason": "aggressive"}

    if classification.get("is_commercial_offer"):
        return {"is_spam": True, "spam_reason": "commercial_offer"}

    return {"is_spam": False, "spam_reason": None}


async def _classify_message(message: str) -> dict:
    prompt = CLASSIFICATION_PROMPT.format(message=message)
    result = await chat_completion([{"role": "user", "content": prompt}], json_mode=True)

    if result["status"] != "text":
        return {"is_aggressive": False, "is_commercial_offer": False}

    try:
        parsed = json.loads(result["content"])
    except (json.JSONDecodeError, TypeError):
        return {"is_aggressive": False, "is_commercial_offer": False}

    # Модель иногда оборачивает объект в список — достаём первый элемент
    if isinstance(parsed, list):
        parsed = parsed[0] if parsed else {}

    if not isinstance(parsed, dict):
        return {"is_aggressive": False, "is_commercial_offer": False}

    return {
        "is_aggressive": bool(parsed.get("is_aggressive", False)),
        "is_commercial_offer": bool(parsed.get("is_commercial_offer", False)),
    }


async def handle_spam(state: AgentState) -> dict:
    """Финальный узел для случая, когда сообщение признано спамом."""
    return {
        "escalate": True,
        "messages": [
            AIMessage(content="Извините, я не могу обработать это сообщение. Передаю ваш запрос менеджеру.")
        ],
    }