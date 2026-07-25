from time import perf_counter

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.evaluations.exact_match import ExactMatchEvaluator
from app.evaluations.exact_match import ExactMatchEvaluator
from app.database.models.experiment import ExperimentStatus
from app.datasets.repository import DatasetRepository
from app.experiments.repository import ExperimentRepository
from app.evaluations.exact_match import ExactMatchEvaluator
from app.experiments.schemas import (
    ExperimentCreate,
    ExperimentResultResponse,
)
from app.providers.factory import ProviderFactory


class ExperimentService:
    def __init__(self, db: Session):
        self.repository = ExperimentRepository(db)
        self.dataset_repository = DatasetRepository(db)

    def create_experiment(
        self,
        request: ExperimentCreate,
    ):
        dataset = self.dataset_repository.get_dataset(
            request.dataset_id
        )

        if dataset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found",
            )

        return self.repository.create_experiment(
            name=request.name,
            description=request.description,
            dataset_id=request.dataset_id,
            provider=request.provider,
            model_name=request.model_name,
        )

    def list_experiments(self):
        return self.repository.list_experiments()

    def run_experiment(self, experiment_id: int):
        experiment = self.repository.get_experiment(
            experiment_id
        )

        if experiment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiment not found",
            )

        dataset = self.dataset_repository.get_dataset(
            experiment.dataset_id
        )

        if dataset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found",
            )

        if not dataset.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dataset has no items",
            )

        try:
            provider = ProviderFactory.create(
                experiment.provider
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

        self.repository.update_status(
            experiment,
            ExperimentStatus.RUNNING,
        )

        results = []

        try:
            for item in dataset.items:
                started_at = perf_counter()

                response = provider.generate(
                    prompt=item.prompt,
                    model=experiment.model_name,
                )

                latency_ms = int(
                    (perf_counter() - started_at) * 1000
                )

                saved_result = self.repository.create_result(
                    experiment_id=experiment.id,
                    dataset_item_id=item.id,
                    model_output=response.text,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    total_tokens=response.total_tokens,
                    cost=response.cost,
                    latency_ms=latency_ms,
                )
                
                exact_match_score = ExactMatchEvaluator.evaluate(
                    model_output=response.text,
                    expected_output=item.expected_output,
                )

                saved_result = self.repository.update_result_scores(
                    result=saved_result,
                    exact_match_score=exact_match_score,
                )

                results.append(
                    {
                        "result_id": saved_result.id,
                        "dataset_item_id": item.id,
                        "model_output": response.text,
                        "input_tokens": response.input_tokens,
                        "output_tokens": response.output_tokens,
                        "total_tokens": response.total_tokens,
                        "cost": response.cost,
                        "latency_ms": latency_ms,
                        "exact_match_score": saved_result.exact_match_score,
                    }
                )

            self.repository.update_status(
                experiment,
                ExperimentStatus.COMPLETED,
            )

        except Exception as exc:
            self.repository.update_status(
                experiment,
                ExperimentStatus.FAILED,
                error_message=str(exc),
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Experiment execution failed",
            ) from exc

        return {
            "experiment_id": experiment.id,
            "status": ExperimentStatus.COMPLETED.value,
            "results": results,
        }

    def get_experiment(self, experiment_id: int):
        experiment = self.repository.get_experiment(
            experiment_id
        )

        if experiment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiment not found",
            )

        return experiment

    def get_experiment_results(
        self,
        experiment_id: int,
    ) -> list[ExperimentResultResponse]:
        experiment = self.repository.get_experiment(
            experiment_id
        )

        if experiment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiment not found",
            )

        results = self.repository.get_results_by_experiment(
            experiment_id
        )

        return [
            ExperimentResultResponse.model_validate(result)
            for result in results
        ]

    def get_result(
        self,
        result_id: int,
    ) -> ExperimentResultResponse:
        result = self.repository.get_result(
            result_id
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiment result not found",
            )

        return ExperimentResultResponse.model_validate(
            result
        )