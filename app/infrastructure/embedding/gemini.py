import asyncio
from typing import List

from google import genai

from app.core.config import Settings
from .base import EmbeddingClient


class GeminiEmbeddingClient(EmbeddingClient):
    def __init__(self, settings: Settings):
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model_name = "gemini-embedding-2"

    async def embed_text(self, text: str) -> List[float]:
        response = await self.client.aio.models.embed_content(
            model=self.model_name,
            contents=text,
        )
        if not response.embeddings or not response.embeddings[0].values:
            return []
        return response.embeddings[0].values

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        # Run multiple embed calls concurrently since a list of strings in 'contents' 
        # is treated as a single multi-part prompt.
        tasks = [self.embed_text(text) for text in texts]
        return await asyncio.gather(*tasks)
