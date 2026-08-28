# agents\state.py
from langgraph.graph import MessagesState
from typing import Optional


class AgentState(MessagesState):
    """MessagesState уже содержит поле `messages: list[BaseMessage]`
    с автоматическим reducer'ом (add_messages), который сам склеивает
    историю диалога — не нужно вручную append'ить."""

    customer: dict
    channel: dict
    summary: str
    agent_name: str
    is_spam: bool
    spam_reason: Optional[str]
    escalate: bool