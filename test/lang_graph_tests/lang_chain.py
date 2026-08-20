import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field

load_dotenv()
os.getenv("OPENROUTER_API_KEY")

model = ChatOpenRouter(
    model = os.getenv("MODEL_NAME"),
    temperature=0,
    max_tokens=1024,
    max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Uzbek. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]

ai_msg = model.invoke(messages)
print(ai_msg.content)


# ==============================================================================
# Tool calling
# ==============================================================================
# from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    """Get the current weather in a given location"""

    location: str = Field(description = "There are a comfortable weather in Tashkent")


model_with_tools = model.bind_tools([GetWeather])

ai_msg = model_with_tools.invoke(
    "what is the weather like in Tashkent",
)
print(ai_msg)