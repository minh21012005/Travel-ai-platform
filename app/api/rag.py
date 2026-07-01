from fastapi import APIRouter, Depends

from app.api.dependencies import get_rag_service
from app.features.rag.schemas import AskRequest, AskResponse
from app.features.rag.service import RAGService

router = APIRouter(tags=["RAG"])

@router.post("/api/v1/rag/ask", response_model=AskResponse)
async def ask_rag(
    req: AskRequest,
    rag_service: RAGService = Depends(get_rag_service),
) -> AskResponse:
    answer, sources = await rag_service.ask_question(
        query=req.query,
        collection_name=req.collection_name,
        filter_metadata=req.filter_metadata,
        limit=req.limit,
    )
    
    return AskResponse(
        answer=answer,
        sources=sources,
    )
