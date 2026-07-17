from fastapi import APIRouter, Depends

from app.api.dependencies import require_role
from app.authentication.roles import UserRole
from app.database.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/test")
def admin_test(
    current_user: User = Depends(
        require_role(UserRole.ADMIN),
    ),
) -> dict[str, str]:
    return {
        "message": "Admin access granted",
        "email": current_user.email,
    }