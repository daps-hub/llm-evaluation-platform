import jwt

from app.authentication.jwt import (
    create_access_token,
    decode_access_token,
)
from app.authentication.password import (
    hash_password,
    verify_password,
)


def test_hash_password() -> None:
    password = "SecurePassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False


def test_create_and_decode_access_token() -> None:
    token = create_access_token(
        subject="user-123",
        additional_claims={
            "role": "engineer",
        },
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "user-123"
    assert payload["role"] == "engineer"
    assert payload["type"] == "access"


def test_decode_invalid_access_token() -> None:
    invalid_token = "not-a-valid-token"

    try:
        decode_access_token(invalid_token)
        assert False, "Expected InvalidTokenError"
    except jwt.InvalidTokenError:
        assert True