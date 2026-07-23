from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.datasets.repository import DatasetRepository
from app.experiments.repository import ExperimentRepository
from app.experiments.schemas import ExperimentCreate
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

        results = []

        for item in dataset.items:
            response = provider.generate(
                prompt=item.prompt,
                model=experiment.model_name,
            )

            results.append(
                {
                    "dataset_item_id": item.id,
                    "model_output": response.text,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "total_tokens": response.total_tokens,
                    "cost": response.cost,
                }
            )

        return {
            "experiment_id": experiment.id,
            "status": "completed",
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