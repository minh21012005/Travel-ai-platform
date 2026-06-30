from app.infrastructure.embedding.base import EmbeddingClient
from app.infrastructure.embedding.utils import cosine_similarity
from app.infrastructure.llm.base import LLMClient
from app.infrastructure.llm.models import LLMRequest


class AIService:
    def __init__(
        self,
        llm: LLMClient,
        embedding: EmbeddingClient,
    ):
        self.llm = llm
        self.embedding = embedding

    async def test(self):

        request = LLMRequest(
            system_prompt="""
                You are a helpful travel assistant.
            """,
            user_prompt="Say hello!",
        )

        return await self.llm.generate(request)

    async def compare_texts(self, text1: str, text2: str) -> float:
        vec1 = await self.embedding.embed_text(text1)
        vec2 = await self.embedding.embed_text(text2)
        return cosine_similarity(vec1, vec2)
