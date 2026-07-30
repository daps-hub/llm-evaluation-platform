from datetime import datetime

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_runs: int
    average_latency_ms: float
    average_tokens: float
    average_cost: float
    average_exact_match: float
    average_semantic_similarity: float
    average_judge_score: float


class CostHistoryItem(BaseModel):
    result_id: int
    run: int
    generation_cost: float
    judge_cost: float
    total_cost: float
    created_at: datetime


class LatencyHistoryItem(BaseModel):
    result_id: int
    run: int
    latency_ms: int
    created_at: datetime


class JudgeScoreHistoryItem(BaseModel):
    result_id: int
    run: int
    judge_score: float
    created_at: datetime


class TokenHistoryItem(BaseModel):
    result_id: int
    run: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    created_at: datetime