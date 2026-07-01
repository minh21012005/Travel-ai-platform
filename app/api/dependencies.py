from fastapi import Depends

from app.core.config import Settings, get_settings
from app.features.ai.service import AIService
from app.features.indexing.service import IndexingService
from app.infrastructure.chunking.base import TextChunker
from app.infrastructure.chunking.recursive import RecursiveTextChunker
from app.infrastructure.embedding.base import EmbeddingClient
from app.infrastructure.embedding.gemini import GeminiEmbeddingClient
from app.infrastructure.llm.base import LLMClient
from app.infrastructure.llm.gemini import GeminiClient
from app.infrastructure.vectordb.base import VectorDBClient
from app.infrastructure.vectordb.qdrant import QdrantDBClient


def get_llm_client(settings: Settings = Depends(get_settings)) -> LLMClient:
    return GeminiClient(settings=settings)


def get_embedding_client(settings: Settings = Depends(get_settings)) -> EmbeddingClient:
    return GeminiEmbeddingClient(settings=settings)


def get_chunker() -> TextChunker:
    # Use default params (1000, 200) or configure from settings
    return RecursiveTextChunker()


def get_ai_service(
    llm: LLMClient = Depends(get_llm_client),
    embedding: EmbeddingClient = Depends(get_embedding_client),
    chunker: TextChunker = Depends(get_chunker),
) -> AIService:
    return AIService(llm=llm, embedding=embedding, chunker=chunker)


def get_vectordb_client(settings: Settings = Depends(get_settings)) -> VectorDBClient:
    return QdrantDBClient(settings=settings)


def get_indexing_service(
    chunker: TextChunker = Depends(get_chunker),
    embedding: EmbeddingClient = Depends(get_embedding_client),
    vectordb: VectorDBClient = Depends(get_vectordb_client),
) -> IndexingService:
    return IndexingService(chunker=chunker, embedding=embedding, vectordb=vectordb)
