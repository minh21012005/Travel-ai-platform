from typing import List

from google import genai

from app.core.config import Settings
from .base import EmbeddingClient


class GeminiEmbeddingClient(EmbeddingClient):
    def __init__(self, settings: Settings):
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model_name = "gemini-embedding-2"

    async def embed_text(self, text: str) -> List[float]:
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
        )
        if not response.embeddings or not response.embeddings[0].values:
            return []
        return response.embeddings[0].values

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=texts,
        )
        if not response.embeddings:
            return []
        return [emb.values for emb in response.embeddings if emb.values]
