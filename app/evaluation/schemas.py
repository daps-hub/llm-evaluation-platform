import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EvaluationCreate(BaseModel):
    model: str = Field(
        min_length=1,
        max_length=100,
    )
    prompt: str = Field(
        min_length=1,
    )


class EvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    model: str
    prompt: str
    response: str
    latency_ms: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    status: str
    created_at: datetime