from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.dependencies import get_ai_service, get_indexing_service
from app.features.ai.service import AIService
from app.features.indexing.schemas import DocumentMetadata
from app.features.indexing.service import IndexingService
from app.infrastructure.llm.models import LLMResponse

router = APIRouter(tags=["Test"])


@router.get("/api/v1/ai/test", response_model=LLMResponse)
async def test(ai_service: AIService = Depends(get_ai_service)) -> LLMResponse:
    return await ai_service.test()


class CompareRequest(BaseModel):
    text1: str
    text2: str

class CompareResponse(BaseModel):
    similarity: float
    text1: str
    text2: str

@router.post("/api/v1/ai/test/embedding", response_model=CompareResponse)
async def test_embedding(
    req: CompareRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> CompareResponse:
    similarity = await ai_service.compare_texts(req.text1, req.text2)
    
    return CompareResponse(
        similarity=similarity,
        text1=req.text1,
        text2=req.text2
    )


class ChunkRequest(BaseModel):
    text: str

class ChunkResponse(BaseModel):
    chunks: list[str]
    count: int

@router.post("/api/v1/ai/test/chunking", response_model=ChunkResponse)
async def test_chunking(
    req: ChunkRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> ChunkResponse:
    chunks = ai_service.chunk_text(req.text)
    
    return ChunkResponse(
        chunks=chunks,
        count=len(chunks)
    )


class IndexRequest(BaseModel):
    text: str
    metadata: DocumentMetadata
    collection_name: str = "travel_docs"

class IndexResponse(BaseModel):
    chunks_indexed: int
    collection_name: str

@router.post("/api/v1/indexing/test", response_model=IndexResponse)
async def test_indexing(
    req: IndexRequest,
    indexing_service: IndexingService = Depends(get_indexing_service),
) -> IndexResponse:
    count = await indexing_service.index_document(req.text, req.metadata, req.collection_name)
    
    return IndexResponse(
        chunks_indexed=count,
        collection_name=req.collection_name
    )
