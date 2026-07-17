from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.authentication.password import hash_password
from app.authentication.schemas import UserRegister, UserResponse
from app.database.connection import get_db
from app.database.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserRegister,
    db: Session = Depends(get_db),
) -> User:
    existing_user = db.scalar(
        select(User).where(User.email == payload.email.lower())
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        role="viewer",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user