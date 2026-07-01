from langchain_text_splitters import RecursiveCharacterTextSplitter

from .base import TextChunker


class RecursiveTextChunker(TextChunker):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split(self, text: str) -> list[str]:
        return self._splitter.split_text(text)
