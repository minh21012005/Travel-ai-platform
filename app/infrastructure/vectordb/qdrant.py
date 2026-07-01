import uuid
from typing import Any

from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse

from app.core.config import Settings
from .base import VectorDBClient


class QdrantDBClient(VectorDBClient):
    def __init__(self, settings: Settings):
        self.client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    async def _ensure_collection_exists(self, collection_name: str, vector_size: int):
        try:
            await self.client.get_collection(collection_name=collection_name)
        except (UnexpectedResponse, ValueError):
            await self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                ),
            )

    async def upsert_vectors(
        self,
        collection_name: str,
        vectors: list[list[float]],
        payloads: list[dict[str, Any]] | None = None,
    ) -> None:
        if not vectors:
            return

        vector_size = len(vectors[0])
        await self._ensure_collection_exists(collection_name, vector_size)

        points = []
        for i, vector in enumerate(vectors):
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payloads[i] if payloads else {},
            )
            points.append(point)

        await self.client.upsert(
            collection_name=collection_name,
            points=points,
        )

    async def search_vectors(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 5,
        filter_metadata: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        
        # Build Qdrant filter if filter_metadata is provided
        qdrant_filter = None
        if filter_metadata:
            must_conditions: list[models.Condition] = [
                models.FieldCondition(key=key, match=models.MatchValue(value=value))
                for key, value in filter_metadata.items()
            ]
            qdrant_filter = models.Filter(must=must_conditions)

        search_result = await self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            query_filter=qdrant_filter,
            with_payload=True,
        )

        # Return just the payloads
        return [hit.payload for hit in search_result.points if hit.payload]
