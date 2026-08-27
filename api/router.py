from fastapi import APIRouter
from core.config import semaphore
from api.schemas import (
    TestConnectionRequest,
    GenerateRequest,
    GenerateResponse,
)
from llm_service import process_message
from services.llm_client import process_message
from services.chat_generation import chat_generation

router = APIRouter()


@router.post("/test_connection_model")
async def ask_llm(request: TestConnectionRequest):
    async with semaphore:
        result = await process_message(request.prompt)
        return {"status": "success", "response": result}


@router.post("/generate", response_model=GenerateResponse)
async def generate_endpoint(request: GenerateRequest):
    async with semaphore:
        result = await chat_generation(request.message, agent_name=request.agent_name)

        return GenerateResponse(
            message=result.get("message", ""),
            summary=result.get("summary", ""),
            escalate=result.get("escalate", False),
            agent_name=result.get("agent_name", request.agent_name),
        )