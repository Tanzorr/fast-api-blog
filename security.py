from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from config import settings

password_hash = PasswordHash.recommended()

# Login checks the password against this hash when the email is unknown. Then a
# wrong email and a wrong password take the same time (no timing attack).
DUMMY_HASH = password_hash.hash("dummy")


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    # JWT wants "sub" as a string (RFC 7519).
    payload = {"sub": str(user_id), "exp": datetime.now(UTC) + expires_delta}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int:
    """Return the user id. Raise jwt.InvalidTokenError for a bad or expired token."""
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
        options={"require": ["sub", "exp"]},
    )
    return int(payload["sub"])
