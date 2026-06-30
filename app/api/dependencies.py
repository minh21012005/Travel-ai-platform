from fastapi import Depends

from app.core.config import Settings, get_settings
from app.features.ai.service import AIService
from app.infrastructure.llm.base import LLMClient
from app.infrastructure.llm.gemini import GeminiClient


def get_llm_client(settings: Settings = Depends(get_settings)) -> LLMClient:
    return GeminiClient(settings=settings)


def get_ai_service(llm: LLMClient = Depends(get_llm_client)) -> AIService:
    return AIService(llm=llm)
