from sqlalchemy.orm import Session

from app.database.models.dataset import Dataset, DatasetItem


class DatasetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_dataset(
        self,
        name: str,
        description: str | None = None,
    ) -> Dataset:
        dataset = Dataset(
            name=name,
            description=description,
        )

        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)

        return dataset

    def list_datasets(self) -> list[Dataset]:
        return (
            self.db.query(Dataset)
            .order_by(Dataset.created_at.desc())
            .all()
        )

    def get_dataset(self, dataset_id: int) -> Dataset | None:
        return (
            self.db.query(Dataset)
            .filter(Dataset.id == dataset_id)
            .first()
        )

    def add_item(
        self,
        dataset_id: int,
        prompt: str,
        expected_output: str,
        metadata: dict | None = None,
    ) -> DatasetItem:
        item = DatasetItem(
            dataset_id=dataset_id,
            prompt=prompt,
            expected_output=expected_output,
            item_metadata=metadata,
        )

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item