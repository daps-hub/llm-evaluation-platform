import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.authentication.dependencies import get_current_user
from app.database.models.user import User
from app.database.connection import get_db
from app.evaluations.schemas import (
    EvaluationCreate,
    EvaluationResponse,
)
from app.evaluations.service import (
    get_evaluation,
    get_evaluations,
    run_evaluation,
)

router = APIRouter(
    prefix="/evaluations",
    tags=["evaluations"],
)


@router.post(
    "",
    response_model=EvaluationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_evaluation(
    evaluation_data: EvaluationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EvaluationResponse:
    return run_evaluation(
        db=db,
        evaluation_data=evaluation_data,
    )


@router.get(
    "",
    response_model=list[EvaluationResponse],
)
def list_all_evaluations(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[EvaluationResponse]:
    return list(
        get_evaluations(
            db,
            offset=offset,
            limit=limit,
        )
    )


@router.get(
    "/{evaluation_id}",
    response_model=EvaluationResponse,
)
def get_single_evaluation(
    evaluation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EvaluationResponse:
    evaluation = get_evaluation(
        db,
        evaluation_id,
    )

    if evaluation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found",
        )

    return evaluation