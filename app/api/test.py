from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.dependencies import get_ai_service
from app.features.ai.service import AIService
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
