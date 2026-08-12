from uuid import UUID
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.authentication.jwt import decode_access_token
from app.database.connection import get_db
from app.database.models.user import User

from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.authentication.roles import UserRole
from app.database.models.user import User

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = UUID(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise credentials_exception

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user

def require_role(
    *allowed_roles: UserRole,
) -> Callable[..., User]:
    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        allowed_values = {role.value for role in allowed_roles}

        if current_user.role not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker