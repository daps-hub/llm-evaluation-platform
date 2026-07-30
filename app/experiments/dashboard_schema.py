from pydantic import BaseModel


class DashboardSummary(BaseModel):

    total_runs: int

    average_latency_ms: float
    average_tokens: float

    average_cost: float

    average_exact_match: float
    average_semantic_similarity: float
    average_judge_score: float