import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

load_dotenv()
os.getenv("OPENROUTER_API_KEY")

model = ChatOpenRouter(
    model = os.getenv("MODEL_NAME"),
    temperature=0,
    max_tokens=1024,
    max_retries=2,
    # other params...
)


msg = HumanMessage(content="Hello world", name="Lance")
messages = [msg]


ai_msg = model.invoke(messages)
print(ai_msg.content)

os.getenv("TAVILY_API_KEY")
from langchain_tavily import TavilySearch  # updated at 1.0

tavily_search = TavilySearch(max_results=3)

data = tavily_search.invoke({"query": "What is LangGraph?"})
search_docs = data.get("results", data)

print(search_docs)