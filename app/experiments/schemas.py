from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.database.models.experiment import ExperimentStatus


class ExperimentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    dataset_id: int
    provider: str = Field(min_length=1, max_length=50)
    model_name: str = Field(min_length=1, max_length=150)


class ExperimentResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    experiment_id: int
    dataset_item_id: int

    model_output: str | None = None

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cost: Decimal | None = None
    latency_ms: int | None = None

    exact_match_score: int | None = None
    semantic_similarity_score: float | None = None
    judge_score: float | None = None
    judge_reasoning: str | None = None
    error_message: str | None = None
    created_at: datetime
    generation_cost: float | None = None
    judge_cost: float | None = None
    total_cost: float | None = None

class ExperimentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    dataset_id: int
    provider: str
    model_name: str
    status: ExperimentStatus
    error_message: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None

    results: list[ExperimentResultResponse] = Field(
        default_factory=list
    )