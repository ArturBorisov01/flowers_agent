# core/config.py

from dotenv import load_dotenv
load_dotenv()

import asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openrouter_api_key: str
    model_name: str
    max_concurrent_requests: int = 5

    # extra="ignore" нужен, чтобы скрипт не падал, если в .env есть другие переменные
    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()

semaphore = asyncio.Semaphore(settings.max_concurrent_requests)