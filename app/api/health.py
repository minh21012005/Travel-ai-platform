from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel


class HealthStatus(str, Enum):
    UP = "UP"


class HealthResponse(BaseModel):
    status: HealthStatus


router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, summary="Health check endpoint")
async def health() -> HealthResponse:
    return HealthResponse(status=HealthStatus.UP)
