import json
from typing import Callable
from agents.state import AgentState
from services.llm_client import chat_completion

MAX_TOOL_ITERATIONS = 3


def make_tool_caller_node(tools_schema: list[dict], tool_functions: dict[str, Callable]):
    async def tool_caller(state: AgentState) -> dict:
        messages = state.get("messages") or _build_initial_messages(state)

        for _ in range(MAX_TOOL_ITERATIONS):
            result = await chat_completion(messages, tools=tools_schema)

            if result["status"] == "error":
                return {"messages": messages, "reply": result["content"], "escalate": True}

            if result["status"] == "text":
                messages.append({"role": "assistant", "content": result["content"]})
                return {"messages": messages, "reply": result["content"]}

            # result["status"] == "tool_call"
            tool_calls = result["calls"]
            messages.append({"role": "assistant", "tool_calls": tool_calls, "content": None})

            for call in tool_calls:
                fn_name = call["function"]["name"]
                fn_args = json.loads(call["function"]["arguments"] or "{}")
                fn = tool_functions.get(fn_name)

                tool_result = (
                    await fn(**fn_args) if fn else f"Тул '{fn_name}' не найден."
                )

                messages.append({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": json.dumps(tool_result, ensure_ascii=False, default=str),
                })

        return {
            "messages": messages,
            "reply": "Не удалось получить ответ: превышен лимит вызовов инструментов.",
            "escalate": True,
        }

    return tool_caller


def _build_initial_messages(state: AgentState) -> list[dict]:
    system_prompt = (
        "Ты — ассистент отдела продаж. Отвечай кратко и по делу. "
        "Используй инструмент search_products, если нужно найти информацию о товарах."
    )
    messages = [{"role": "system", "content": system_prompt}]

    if state.get("summary"):
        messages.append({"role": "system", "content": f"Контекст предыдущего диалога: {state['summary']}"})

    messages.append({"role": "user", "content": state["message"]})
    return messages