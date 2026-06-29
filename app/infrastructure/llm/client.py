from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:

        raise NotImplementedError("Subclasses must implement the generate method.")
