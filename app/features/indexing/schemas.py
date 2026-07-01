import uuid
from typing import Optional
from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    document_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    source: Optional[str] = None
    city: Optional[str] = None
