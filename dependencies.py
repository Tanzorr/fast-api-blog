from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import UserModel
from schemas import Pagination
from security import decode_access_token

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

# Reads "Authorization: Bearer <token>". No header → 401 by itself.
# tokenUrl tells the Authorize button in /docs where to log in.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    credentials_error = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise credentials_error from None
    user = db.get(UserModel, user_id)
    if user is None:
        raise credentials_error
    return user


def get_pagination(
    limit: Annotated[int, Query(ge=1, le=MAX_LIMIT)] = DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Pagination:
    # A value out of range → 422 by itself, before the endpoint runs.
    return Pagination(limit=limit, offset=offset)
