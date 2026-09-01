# Pydantic models
from pydantic import BaseModel, Field
from typing import Optional

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    session_id: Optional[str] = None
    stream: bool = False  # Placeholder for future SSE implementation
    force_route: Optional[str] = Field(None, pattern="^(LOCAL|CLOUD)$")

class GenerateResponse(BaseModel):
    response: str
    route_used: str
    latency_ms: float
    cached: bool = False
    session_id: str