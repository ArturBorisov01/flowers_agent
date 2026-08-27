import re
from agents.state import AgentState

# Строка без единой буквы (только цифры/пробелы/спецсимволы) считается мусором
GARBAGE_PATTERN = re.compile(r"^[\s\d\W]*$")


async def check_spam(state: AgentState) -> dict:
    message = state.get("message", "").strip()
    is_spam = len(message) < 2 or bool(GARBAGE_PATTERN.match(message))
    return {"is_spam": is_spam}