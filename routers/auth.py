from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import UserModel
from schemas import Token
from security import DUMMY_HASH, create_access_token, password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # The OAuth2 form calls the field "username"; here it holds the email (ADR-012).
    user = db.scalar(select(UserModel).where(UserModel.email == form_data.username))
    hashed = user.password if user is not None else DUMMY_HASH
    password_ok = password_hash.verify(form_data.password, hashed)
    if user is None or not password_ok:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.id))
