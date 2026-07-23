from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.datasets.repository import DatasetRepository
from app.experiments.repository import ExperimentRepository
from app.experiments.schemas import ExperimentCreate


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