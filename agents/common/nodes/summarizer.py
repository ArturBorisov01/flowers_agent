# agents/common/nodes/summarizer.py
from agents.state import AgentState
from services.llm_client import chat_completion


async def build_summary(state: AgentState) -> dict:
    print("→ NODE: build_summary")
    prev_summary = state.get("summary", "")
    message, reply = _extract_last_exchange(state["messages"])

    prompt = (
        "Обнови краткое саммари диалога с клиентом (2-3 предложения), "
        "учитывая предыдущее саммари и новый обмен репликами. "
        "Верни только текст саммари, без пояснений.\n\n"
        f"Предыдущее саммари: {prev_summary or 'отсутствует'}\n"
        f"Сообщение клиента: {message}\n"
        f"Ответ агента: {reply}"
    )

    result = await chat_completion([{"role": "user", "content": prompt}])
    print("Debug_summarizer", result)
    print()

    if result["status"] == "text":
        return {"summary": result["content"].strip()}

    return {"summary": prev_summary}


def _extract_last_exchange(messages: list) -> tuple[str, str]:
    print("→ NODE: _extract_last_exchange")
    """Достаёт последнее сообщение клиента (Human) и последний ответ агента (AI)."""
    last_human = ""
    last_ai = ""

    for msg in reversed(messages):
        msg_type = getattr(msg, "type", "")
        if msg_type == "ai" and not last_ai:
            last_ai = msg.content or ""
        elif msg_type == "human" and not last_human:
            last_human = msg.content or ""

        if last_human and last_ai:
            break

    return last_human, last_ai