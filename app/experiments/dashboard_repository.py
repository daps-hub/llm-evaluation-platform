from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models.experiment import ExperimentResult


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def _get_results(self, experiment_id: int) -> list[ExperimentResult]:
        return (
            self.db.query(ExperimentResult)
            .filter(ExperimentResult.experiment_id == experiment_id)
            .order_by(
                ExperimentResult.created_at.asc(),
                ExperimentResult.id.asc(),
            )
            .all()
        )

    def get_summary(self, experiment_id: int):
        results = self._get_results(experiment_id)

        if not results:
            return None

        total_runs = len(results)

        average_latency_ms = (
            sum(result.latency_ms or 0 for result in results) / total_runs
        )

        average_tokens = (
            sum(result.total_tokens or 0 for result in results) / total_runs
        )

        average_cost = (
            sum(float(result.total_cost or 0) for result in results)
            / total_runs
        )

        average_exact_match = (
            sum(float(result.exact_match_score or 0) for result in results)
            / total_runs
        )

        average_semantic_similarity = (
            sum(
                float(result.semantic_similarity_score or 0)
                for result in results
            )
            / total_runs
        )

        average_judge_score = (
            sum(float(result.judge_score or 0) for result in results)
            / total_runs
        )

        return {
            "total_runs": total_runs,
            "average_latency_ms": round(average_latency_ms, 2),
            "average_tokens": round(average_tokens, 2),
            "average_cost": round(average_cost, 6),
            "average_exact_match": round(average_exact_match, 3),
            "average_semantic_similarity": round(
                average_semantic_similarity,
                3,
            ),
            "average_judge_score": round(average_judge_score, 2),
        }

    def get_cost_history(self, experiment_id: int):
        results = self._get_results(experiment_id)

        return [
            {
                "result_id": result.id,
                "run": index,
                "generation_cost": float(
                    result.generation_cost
                    if result.generation_cost is not None
                    else result.cost or 0
                ),
                "judge_cost": float(result.judge_cost or 0),
                "total_cost": float(
                    result.total_cost
                    if result.total_cost is not None
                    else result.cost or 0
                ),
                "created_at": result.created_at,
            }
            for index, result in enumerate(results, start=1)
        ]

    def get_latency_history(self, experiment_id: int):
        results = self._get_results(experiment_id)

        return [
            {
                "result_id": result.id,
                "run": index,
                "latency_ms": result.latency_ms or 0,
                "created_at": result.created_at,
            }
            for index, result in enumerate(results, start=1)
        ]

    def get_judge_score_history(self, experiment_id: int):
        results = self._get_results(experiment_id)

        return [
            {
                "result_id": result.id,
                "run": index,
                "judge_score": float(result.judge_score or 0),
                "created_at": result.created_at,
            }
            for index, result in enumerate(results, start=1)
        ]

    def get_token_history(self, experiment_id: int):
        results = self._get_results(experiment_id)

        return [
            {
                "result_id": result.id,
                "run": index,
                "input_tokens": result.input_tokens or 0,
                "output_tokens": result.output_tokens or 0,
                "total_tokens": result.total_tokens or 0,
                "created_at": result.created_at,
            }
            for index, result in enumerate(results, start=1)
        ]