import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from llm_service import process_message
from summar import summary_message
from chat_model import chat_generation

app = FastAPI()

# Ограничение конкурентных запросов к API
MAX_CONCURRENT_REQUESTS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS) 

class AskRequest(BaseModel):
    prompt: str = 'привет'

class SummarRequest(BaseModel):
    user_id: int | None = None
    session_id: int| None = None
    new_massage: str = "хочу купить подсолнухи"

class GenerateRequest(BaseModel):
    collection_name: str | None = None
    query: str

@app.post("/ask")
async def ask_llm(request: AskRequest):
    # Ограничиваем одновременный доступ к LLM через семафор
    async with semaphore:
        result = await process_message(request.prompt)
        return {"status": "success", "response": result}


old_summary = 'Клиента зовут Петя и он спрашивал о цветах, которые есть в наличии. В наличии есть розы.'

@app.post("/summar")
async def summar_message_endpoint(request: SummarRequest):
    async with semaphore:

        result = await summary_message(old_summary, request.new_massage)
        return {"status": "success", "response": result}


@app.post("/generate")
async def generate_endpoint(request: GenerateRequest):
    async with semaphore:
    
        result = await chat_generation(request.query)
        return {"status": "success", "response": result}


# http://192.168.2.97:8000