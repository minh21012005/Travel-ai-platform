from app.infrastructure.llm.base import LLMClient
from app.infrastructure.llm.models import LLMRequest


class AIService:
    def __init__(
        self,
        llm: LLMClient,
    ):
        self.llm = llm

    async def test(self):

        request = LLMRequest(
            system_prompt="""
                You are a helpful travel assistant.
            """,
            user_prompt="Say hello!",
        )

        return await self.llm.generate(request)
