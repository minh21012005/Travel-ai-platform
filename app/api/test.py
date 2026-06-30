from fastapi import APIRouter, Depends

from app.api.dependencies import get_ai_service
from app.features.ai.service import AIService
from app.infrastructure.llm.models import LLMResponse

router = APIRouter(tags=["Test"])


@router.get("/api/v1/ai/test", response_model=LLMResponse)
async def test(ai_service: AIService = Depends(get_ai_service)) -> LLMResponse:
    return await ai_service.test()
