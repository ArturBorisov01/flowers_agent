import httpx

SEARCH_URL = "http://10.175.252.240:3000/product/search"


async def search_products(query: str) -> list:
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            response = await client.get(
                SEARCH_URL,
                headers={"accept": "*/*"},
                params={"limit": 5, "q": query},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return [{"error": str(e)}]


# Схема тула для OpenRouter/OpenAI tool-calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Ищет товары в каталоге по текстовому запросу клиента.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"}
                },
                "required": ["query"],
            },
        },
    }
]

TOOL_FUNCTIONS = {"search_products": search_products}