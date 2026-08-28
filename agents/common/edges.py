from agents.state import AgentState


def route_after_spam_check(state: AgentState) -> str:
    print("DEBUG state in edge:", state.get("is_spam"))
    return "spam" if state.get("is_spam") else "ok"