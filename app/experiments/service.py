from time import perf_counter

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database.models.experiment import ExperimentStatus
from app.datasets.repository import DatasetRepository
from app.evaluations import (
    ExactMatchEvaluator,
    LLMJudgeEvaluator,
    SemanticSimilarityEvaluator,
)
from app.experiments.repository import ExperimentRepository
from app.experiments.schemas import (
    ExperimentCreate,
    ExperimentResultResponse,
)
from app.providers.factory import ProviderFactory


class ExperimentService:
    def __init__(self, db: Session):
        self.repository = ExperimentRepository(db)
        self.dataset_repository = DatasetRepository(db)
        self.judge_evaluator = LLMJudgeEvaluator()

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

    def run_experiment(
        self,
        experiment_id: int,
    ):
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

                generation_cost = float(
                    response.cost or 0.0
                )

                saved_result = self.repository.create_result(
                    experiment_id=experiment.id,
                    dataset_item_id=item.id,
                    model_output=response.text,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    total_tokens=response.total_tokens,
                    cost=generation_cost,
                    generation_cost=generation_cost,
                    judge_cost=0.0,
                    total_cost=generation_cost,
                    latency_ms=latency_ms,
                )

                exact_match_score = (
                    ExactMatchEvaluator.evaluate(
                        model_output=response.text,
                        expected_output=item.expected_output,
                    )
                )

                semantic_similarity_score = (
                    SemanticSimilarityEvaluator.evaluate(
                        expected_output=item.expected_output,
                        model_output=response.text,
                    )
                )

                judge_result = (
                    self.judge_evaluator.evaluate(
                        prompt=item.prompt,
                        expected_output=item.expected_output,
                        model_output=response.text,
                    )
                )

                judge_score = float(
                    judge_result["score"]
                )

                judge_reasoning = str(
                    judge_result["reasoning"]
                )

                judge_cost = float(
                    judge_result.get("judge_cost", 0.0)
                    or 0.0
                )

                total_cost = round(
                    generation_cost + judge_cost,
                    10,
                )

                saved_result = (
                    self.repository.update_result_scores(
                        result=saved_result,
                        exact_match_score=exact_match_score,
                        semantic_similarity_score=(
                            semantic_similarity_score
                        ),
                        judge_score=judge_score,
                        judge_reasoning=judge_reasoning,
                        generation_cost=generation_cost,
                        judge_cost=judge_cost,
                        total_cost=total_cost,
                    )
                )

                results.append(
                    {
                        "result_id": saved_result.id,
                        "dataset_item_id": item.id,
                        "model_output": (
                            saved_result.model_output
                        ),
                        "input_tokens": (
                            saved_result.input_tokens
                        ),
                        "output_tokens": (
                            saved_result.output_tokens
                        ),
                        "total_tokens": (
                            saved_result.total_tokens
                        ),
                        "cost": saved_result.cost,
                        "generation_cost": (
                            saved_result.generation_cost
                        ),
                        "judge_cost": (
                            saved_result.judge_cost
                        ),
                        "total_cost": (
                            saved_result.total_cost
                        ),
                        "latency_ms": (
                            saved_result.latency_ms
                        ),
                        "exact_match_score": (
                            saved_result.exact_match_score
                        ),
                        "semantic_similarity_score": (
                            saved_result
                            .semantic_similarity_score
                        ),
                        "judge_score": (
                            saved_result.judge_score
                        ),
                        "judge_reasoning": (
                            saved_result.judge_reasoning
                        ),
                        "judge_model": judge_result.get(
                            "judge_model"
                        ),
                        "judge_input_tokens": (
                            judge_result.get(
                                "judge_input_tokens",
                                0,
                            )
                        ),
                        "judge_output_tokens": (
                            judge_result.get(
                                "judge_output_tokens",
                                0,
                            )
                        ),
                        "judge_total_tokens": (
                            judge_result.get(
                                "judge_total_tokens",
                                0,
                            )
                        ),
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
                status_code=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=(
                    "Experiment execution failed: "
                    f"{exc}"
                ),
            ) from exc

        return {
            "experiment_id": experiment.id,
            "status": ExperimentStatus.COMPLETED.value,
            "results": results,
        }

    def get_experiment(
        self,
        experiment_id: int,
    ):
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

        results = (
            self.repository.get_results_by_experiment(
                experiment_id
            )
        )

        return [
            ExperimentResultResponse.model_validate(
                result
            )
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