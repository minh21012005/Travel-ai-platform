from typing import Any, Optional

from app.infrastructure.embedding.base import EmbeddingClient
from app.infrastructure.llm.base import LLMClient
from app.infrastructure.llm.models import LLMRequest
from app.infrastructure.vectordb.base import VectorDBClient

class RAGService:
    def __init__(
        self,
        embedding: EmbeddingClient,
        vectordb: VectorDBClient,
        llm: LLMClient,
    ):
        self.embedding = embedding
        self.vectordb = vectordb
        self.llm = llm

    def _build_system_prompt(self, sources: list[dict[str, Any]]) -> str:
        """
        Builds a system prompt containing all the context from the retrieved documents.
        """
        if not sources:
            return "You are an AI assistant. Please answer the user's question based on your general knowledge since no specific documents were found."

        prompt = "You are a helpful travel assistant. Please answer the user's question based ONLY on the provided context below.\n\n"
        prompt += "CONTEXT:\n"
        prompt += "-" * 40 + "\n"
        for idx, source in enumerate(sources):
            content = source.get("content", "")
            title = source.get("title", "Unknown Title")
            prompt += f"Document [{idx + 1}] - Title: {title}\n{content}\n\n"
        
        prompt += "-" * 40 + "\n"
        prompt += "If the answer cannot be found in the context, politely say that you don't have enough information."
        return prompt

    async def ask_question(
        self, 
        query: str, 
        collection_name: str = "travel_docs",
        filter_metadata: Optional[dict[str, Any]] = None,
        limit: int = 5
    ) -> tuple[str, list[dict[str, Any]]]:
        
        # 1. Embed the query
        query_vector = await self.embedding.embed_text(query)

        # 2. Search for top K most relevant documents
        sources = await self.vectordb.search_vectors(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            filter_metadata=filter_metadata,
        )

        # 3. Build prompt with context
        system_prompt = self._build_system_prompt(sources)
        llm_request = LLMRequest(
            system_prompt=system_prompt,
            user_prompt=query,
        )

        # 4. Generate response
        llm_response = await self.llm.generate(llm_request)

        return llm_response.text, sources
