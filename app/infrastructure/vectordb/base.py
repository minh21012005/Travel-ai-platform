from abc import ABC, abstractmethod
from typing import Any


class VectorDBClient(ABC):
    @abstractmethod
    async def upsert_vectors(
        self,
        collection_name: str,
        vectors: list[list[float]],
        payloads: list[dict[str, Any]] | None = None,
    ) -> None:
        pass
