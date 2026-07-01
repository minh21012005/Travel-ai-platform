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

    @abstractmethod
    async def search_vectors(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 5,
        filter_metadata: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Searches for the closest vectors and returns their payloads.
        """
        pass
