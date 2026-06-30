from abc import ABC, abstractmethod

from .models import LLMRequest, LLMResponse


class LLMClient(ABC):
    @abstractmethod
    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        pass
