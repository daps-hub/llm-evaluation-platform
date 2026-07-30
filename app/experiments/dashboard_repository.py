from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models.experiment import ExperimentResult


class DashboardRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_summary(self, experiment_id: int):

        results = (
            self.db.query(ExperimentResult)
            .filter(
                ExperimentResult.experiment_id == experiment_id
            )
            .all()
        )

        if not results:
            return None

        total_runs = len(results)

        avg_latency = sum(r.latency_ms or 0 for r in results) / total_runs
        avg_tokens = sum(r.total_tokens or 0 for r in results) / total_runs
        avg_cost = sum(float(r.total_cost or 0) for r in results) / total_runs

        avg_exact = sum(r.exact_match_score or 0 for r in results) / total_runs
        avg_semantic = sum(r.semantic_similarity_score or 0 for r in results) / total_runs
        avg_judge = sum(r.judge_score or 0 for r in results) / total_runs

        return {
            "total_runs": total_runs,
            "average_latency_ms": round(avg_latency, 2),
            "average_tokens": round(avg_tokens, 2),
            "average_cost": round(avg_cost, 6),
            "average_exact_match": round(avg_exact, 3),
            "average_semantic_similarity": round(avg_semantic, 3),
            "average_judge_score": round(avg_judge, 2),
        }