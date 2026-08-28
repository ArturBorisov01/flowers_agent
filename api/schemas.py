# api\schemas.py

from typing import Optional
from pydantic import BaseModel


class TestConnectionRequest(BaseModel):
    prompt: str = "привет"


class Customer(BaseModel):
    id: int = 1
    name: Optional[str] = None
    phone: Optional[str] = None


class Channel(BaseModel):
    type: str
    chatId: str = '1'


class GenerateRequest(BaseModel):
    customer: Customer
    channel: Channel
    message: str
    summary: Optional[str] = None
    agent_name: str = 'sales'


class GenerateResponse(BaseModel):
    message: str
    summary: str
    escalate: bool = False
    agent_name: str