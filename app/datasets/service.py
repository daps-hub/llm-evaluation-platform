from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.datasets.repository import DatasetRepository
from app.datasets.schemas import DatasetCreate, DatasetItemCreate


class DatasetService:
    def __init__(self, db: Session):
        self.repository = DatasetRepository(db)

    def create_dataset(self, request: DatasetCreate):
        return self.repository.create_dataset(
            name=request.name,
            description=request.description,
        )

    def list_datasets(self):
        return self.repository.list_datasets()

    def get_dataset(self, dataset_id: int):
        dataset = self.repository.get_dataset(dataset_id)

        if dataset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found",
            )

        return dataset

    def add_item(
        self,
        dataset_id: int,
        request: DatasetItemCreate,
    ):
        self.get_dataset(dataset_id)

        return self.repository.add_item(
            dataset_id=dataset_id,
            prompt=request.prompt,
            expected_output=request.expected_output,
            metadata=request.metadata,
        )