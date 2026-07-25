from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.experiments.schemas import (
    ExperimentCreate,
    ExperimentResponse,
    ExperimentResultResponse,
)
from app.experiments.service import ExperimentService


router = APIRouter(
    prefix="/experiments",
    tags=["Experiments"],
)


@router.post(
    "",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experiment(
    request: ExperimentCreate,
    db: Session = Depends(get_db),
):
    return ExperimentService(db).create_experiment(request)


@router.get(
    "",
    response_model=list[ExperimentResponse],
)
def list_experiments(
    db: Session = Depends(get_db),
):
    return ExperimentService(db).list_experiments()


@router.get(
    "/{experiment_id}",
    response_model=ExperimentResponse,
)
def get_experiment(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    return ExperimentService(db).get_experiment(
        experiment_id
    )


@router.post(
    "/{experiment_id}/run",
    status_code=status.HTTP_200_OK,
)
def run_experiment(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    return ExperimentService(db).run_experiment(
        experiment_id
    )


@router.get(
    "/{experiment_id}/results",
    response_model=list[ExperimentResultResponse],
    status_code=status.HTTP_200_OK,
)
def get_experiment_results(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    return ExperimentService(db).get_experiment_results(
        experiment_id
    )


@router.get(
    "/results/{result_id}",
    response_model=ExperimentResultResponse,
    status_code=status.HTTP_200_OK,
)
def get_experiment_result(
    result_id: int,
    db: Session = Depends(get_db),
):
    return ExperimentService(db).get_result(
        result_id
    )