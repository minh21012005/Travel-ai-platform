from app.features.indexing.schemas import DocumentMetadata
from app.infrastructure.chunking.base import TextChunker
from app.infrastructure.embedding.base import EmbeddingClient
from app.infrastructure.vectordb.base import VectorDBClient


class IndexingService:
    def __init__(
        self,
        chunker: TextChunker,
        embedding: EmbeddingClient,
        vectordb: VectorDBClient,
    ):
        self.chunker = chunker
        self.embedding = embedding
        self.vectordb = vectordb

    async def index_document(
        self, 
        text: str, 
        metadata: DocumentMetadata,
        collection_name: str = "travel_docs"
    ) -> int:
        """
        Indexes a document by chunking it, embedding the chunks, and saving them to the vector DB.
        Returns the number of chunks indexed.
        """
        # 1. Chunk the document
        chunks = self.chunker.split(text)
        if not chunks:
            return 0

        # 2. Embed the chunks
        vectors = await self.embedding.embed_batch(chunks)

        # 3. Prepare payloads with metadata
        payloads = []
        for i, chunk in enumerate(chunks):
            payload = metadata.model_dump()
            payload["chunk_index"] = i
            payload["content"] = chunk
            payloads.append(payload)

        # 4. Upsert to Vector Database
        await self.vectordb.upsert_vectors(
            collection_name=collection_name,
            vectors=vectors,
            payloads=payloads,
        )

        return len(chunks)
