from typing import Any, Optional
from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str
    collection_name: str = "travel_docs"
    filter_metadata: Optional[dict[str, Any]] = None
    limit: int = 5

class AskResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]]
