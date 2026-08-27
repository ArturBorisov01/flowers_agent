from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):
    message: str          # входящее сообщение клиента
    summary: str            # саммари диалога (входит и обновляется)
    customer: dict
    channel: dict
    agent_name: str
    is_spam: bool
    messages: list[dict]     # история для tool-calling loop (формат OpenAI)
    reply: str                # финальный ответ агента
    escalate: bool