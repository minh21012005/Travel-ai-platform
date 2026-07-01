from abc import ABC, abstractmethod


class TextChunker(ABC):
    @abstractmethod
    def split(
        self,
        text: str,
    ) -> list[str]: ...
