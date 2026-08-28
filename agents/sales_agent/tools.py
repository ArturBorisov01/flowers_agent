import httpx

SEARCH_URL = "http://10.175.252.240:3000/products/search"


async def search_products(query: str) -> list:
    """Ищет товары в каталоге по текстовому запросу клиента.

    Args:
        query: поисковый запрос клиента
    """
    print(f"→ TOOL: search_products(query={query!r})")

    async with httpx.AsyncClient(timeout=5) as client:
        try:
            response = await client.get(
                SEARCH_URL,
                headers={"accept": "*/*"},
                params={"limit": 5, "q": query},
            )
            response.raise_for_status()
            result = response.json()
            print(f"← TOOL: search_products returned {result}")
            return result
        except httpx.HTTPError as e:
            print(f"← TOOL: search_products ERROR {e}")
            return [{"error": str(e)}]

TOOLS = [search_products]