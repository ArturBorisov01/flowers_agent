from agents.sales_agent.graph import build_graph as build_sales_graph

_REGISTRY = {
    "sales": build_sales_graph(),
}


def get_agent_graph(agent_name: str):
    if agent_name not in _REGISTRY:
        raise ValueError(f"Unknown agent_name: {agent_name}")
    return _REGISTRY[agent_name]