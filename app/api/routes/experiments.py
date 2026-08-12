from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.experiments.dashboard_schema import DashboardSummary
from app.experiments.dashboard_service import DashboardService
from app.experiments.dashboard_schema import (
    CostHistoryItem,
    DashboardSummary,
    JudgeScoreHistoryItem,
    LatencyHistoryItem,
    TokenHistoryItem,
)
from app.experiments.dashboard_service import DashboardService
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

@router.get(
    "/{experiment_id}/dashboard",
    response_model=DashboardSummary,
)
def dashboard(
    experiment_id: int,
    db: Session = Depends(get_db),
):

    service = DashboardService(db)

    return service.summary(experiment_id)

@router.get(
    "/{experiment_id}/dashboard",
    response_model=DashboardSummary,
)
def get_dashboard_summary(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    summary = service.summary(experiment_id)

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="No results found for this experiment",
        )

    return summary


@router.get(
    "/{experiment_id}/dashboard/cost-history",
    response_model=list[CostHistoryItem],
)
def get_cost_history(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.cost_history(experiment_id)


@router.get(
    "/{experiment_id}/dashboard/latency-history",
    response_model=list[LatencyHistoryItem],
)
def get_latency_history(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.latency_history(experiment_id)


@router.get(
    "/{experiment_id}/dashboard/judge-score-history",
    response_model=list[JudgeScoreHistoryItem],
)
def get_judge_score_history(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.judge_score_history(experiment_id)


@router.get(
    "/{experiment_id}/dashboard/token-history",
    response_model=list[TokenHistoryItem],
)
def get_token_history(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    service = DashboardService(db)
    return service.token_history(experiment_id)