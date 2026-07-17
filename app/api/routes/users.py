from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.authentication.schemas import UserResponse
from app.database.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user