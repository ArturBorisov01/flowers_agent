from agents.state import AgentState
from services.llm_client import chat_completion


async def build_summary(state: AgentState) -> dict:
    prev_summary = state.get("summary", "")
    reply = state.get("reply", "")
    message = state.get("message", "")

    prompt = (
        "Обнови краткое саммари диалога с клиентом (2-3 предложения), "
        "учитывая предыдущее саммари и новый обмен репликами. "
        "Верни только текст саммари, без пояснений.\n\n"
        f"Предыдущее саммари: {prev_summary or 'отсутствует'}\n"
        f"Сообщение клиента: {message}\n"
        f"Ответ агента: {reply}"
    )

    result = await chat_completion([{"role": "user", "content": prompt}])

    if result["status"] == "text":
        return {"summary": result["content"].strip()}

    return {"summary": prev_summary}