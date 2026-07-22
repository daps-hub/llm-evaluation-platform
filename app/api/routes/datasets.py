from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.datasets.schemas import (
    DatasetCreate,
    DatasetItemCreate,
    DatasetItemResponse,
    DatasetResponse,
)
from app.datasets.service import DatasetService

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


@router.post(
    "",
    response_model=DatasetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_dataset(
    request: DatasetCreate,
    db: Session = Depends(get_db),
):
    return DatasetService(db).create_dataset(request)


@router.get(
    "",
    response_model=list[DatasetResponse],
)
def list_datasets(
    db: Session = Depends(get_db),
):
    return DatasetService(db).list_datasets()


@router.get(
    "/{dataset_id}",
    response_model=DatasetResponse,
)
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    return DatasetService(db).get_dataset(dataset_id)


@router.post(
    "/{dataset_id}/items",
    response_model=DatasetItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_dataset_item(
    dataset_id: int,
    request: DatasetItemCreate,
    db: Session = Depends(get_db),
):
    return DatasetService(db).add_item(
        dataset_id=dataset_id,
        request=request,
    )