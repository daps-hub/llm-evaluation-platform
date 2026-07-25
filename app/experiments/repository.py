from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session, selectinload

from app.database.models.experiment import (
    Experiment,
    ExperimentResult,
    ExperimentStatus,
)


class ExperimentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_experiment(
        self,
        name: str,
        dataset_id: int,
        provider: str,
        model_name: str,
        description: str | None = None,
    ) -> Experiment:
        experiment = Experiment(
            name=name,
            description=description,
            dataset_id=dataset_id,
            provider=provider,
            model_name=model_name,
            status=ExperimentStatus.CREATED,
        )

        self.db.add(experiment)
        self.db.commit()
        self.db.refresh(experiment)

        return experiment

    def list_experiments(self) -> list[Experiment]:
        return (
            self.db.query(Experiment)
            .options(selectinload(Experiment.results))
            .order_by(Experiment.created_at.desc())
            .all()
        )

    def get_experiment(
        self,
        experiment_id: int,
    ) -> Experiment | None:
        return (
            self.db.query(Experiment)
            .options(selectinload(Experiment.results))
            .filter(Experiment.id == experiment_id)
            .first()
        )

    def update_status(
        self,
        experiment: Experiment,
        status: ExperimentStatus,
        error_message: str | None = None,
    ) -> Experiment:
        experiment.status = status
        experiment.error_message = error_message

        if status == ExperimentStatus.RUNNING:
            experiment.started_at = datetime.utcnow()
            experiment.completed_at = None

        elif status == ExperimentStatus.COMPLETED:
            experiment.completed_at = datetime.utcnow()
            experiment.error_message = None

        elif status == ExperimentStatus.FAILED:
            experiment.completed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(experiment)

        return experiment

    def create_result(
        self,
        *,
        experiment_id: int,
        dataset_item_id: int,
        model_output: str | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        total_tokens: int | None = None,
        cost: Decimal | float | None = None,
        exact_match_score: int | None = None,
        semantic_similarity_score: str | None = None,
        judge_score: str | None = None,
        latency_ms: int | None = None,
        error_message: str | None = None,
    ) -> ExperimentResult:
        result = ExperimentResult(
            experiment_id=experiment_id,
            dataset_item_id=dataset_item_id,
            model_output=model_output,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost=cost,
            exact_match_score=exact_match_score,
            semantic_similarity_score=semantic_similarity_score,
            judge_score=judge_score,
            latency_ms=latency_ms,
            error_message=error_message,
        )

        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result

    def get_results_by_experiment(
        self,
        experiment_id: int,
    ) -> list[ExperimentResult]:
        return (
            self.db.query(ExperimentResult)
            .filter(
                ExperimentResult.experiment_id == experiment_id
            )
            .order_by(ExperimentResult.created_at.asc())
            .all()
        )

    def get_result(
        self,
        result_id: int,
    ) -> ExperimentResult | None:
        return (
            self.db.query(ExperimentResult)
            .filter(ExperimentResult.id == result_id)
            .first()
        )