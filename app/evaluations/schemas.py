import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EvaluationCreate(BaseModel):
    provider: str = Field(
        default="mock",
        min_length=1,
        max_length=50,
    )

    model: str = Field(
        min_length=1,
        max_length=100,
    )

    prompt: str = Field(
        min_length=1,
    )

    expected_response: str | None = Field(
        default=None,
    )


class EvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    provider: str
    model: str
    prompt: str
    expected_response: str | None
    actual_response: str
    latency_ms: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    status: str
    created_at: datetime
    semantic_similarity: float | None = None
    correctness_score: float | None = None
    hallucination_score: float | None = None
    overall_score: float | None = None
    relevance_score: float | None = None
    judge_reasoning: str | None = None