from fastapi import Depends

from app.core.config import Settings, get_settings
from app.features.ai.service import AIService
from app.infrastructure.embedding.base import EmbeddingClient
from app.infrastructure.embedding.gemini import GeminiEmbeddingClient
from app.infrastructure.llm.base import LLMClient
from app.infrastructure.llm.gemini import GeminiClient


def get_llm_client(settings: Settings = Depends(get_settings)) -> LLMClient:
    return GeminiClient(settings=settings)


def get_embedding_client(settings: Settings = Depends(get_settings)) -> EmbeddingClient:
    return GeminiEmbeddingClient(settings=settings)


def get_ai_service(
    llm: LLMClient = Depends(get_llm_client),
    embedding: EmbeddingClient = Depends(get_embedding_client)
) -> AIService:
    return AIService(llm=llm, embedding=embedding)
