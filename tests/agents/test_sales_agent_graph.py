# tests/agents/test_sales_agent_graph.py
from core.config import settings
# settings тут нужен иначе не видит ключ
import asyncio
from services.chat_generation import chat_generation

async def main():
    result = await chat_generation("Есть ли у вас беспроводные наушники?", agent_name="sales")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())