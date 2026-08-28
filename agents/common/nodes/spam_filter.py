# agents\common\nodes\spam_filter.py
import json
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
    message = state.get("message", "").strip()

    # 1. Проверка длины 
    if len(message) == 0 or len(message) > MAX_MESSAGE_LENGTH:
        print("DEBUG: спам по длине")
        return {"is_spam": True, "spam_reason": "invalid_length"}

    # 2. Проверка агрессии и коммерческого предложения — одним LLM-запросом
    classification = await _classify_message(message)
    print("DEBUG classification:", classification) 

    if classification.get("is_aggressive"):
        return {"is_spam": True, "spam_reason": "aggressive"}

    if classification.get("is_commercial_offer"):
        return {"is_spam": True, "spam_reason": "commercial_offer"}

    return {"is_spam": False, "spam_reason": None}


async def _classify_message(message: str) -> dict:
    prompt = CLASSIFICATION_PROMPT.format(message=message)
    
    result = await chat_completion([{"role": "user", "content": prompt}])
    print("DEBUG raw LLM response:", result)

    if result["status"] != "text":
        # Если LLM недоступна — не блокируем сообщение, пропускаем дальше
        return {"is_aggressive": False, "is_commercial_offer": False}

    try:
        return json.loads(result["content"])
    except (json.JSONDecodeError, TypeError):
        # Модель вернула не-JSON — считаем сообщение не спамом, не блокируем клиента
        return {"is_aggressive": False, "is_commercial_offer": False}

async def handle_spam(state: AgentState) -> dict:
    """Финальный узел для случая, когда сообщение признано спамом."""
    return {
        "escalate": True,
        "reply": "",
    }