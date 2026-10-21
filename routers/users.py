from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import UserModel
from schemas import User, UserOut
from security import password_hash

router = APIRouter(prefix="/users", tags=["users"])


def get_user_or_404(user_id: int, db: Session) -> UserModel:
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


def commit_user(user: UserModel, db: Session) -> UserModel:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Email {user.email} is already registered")
    db.refresh(user)
    return user


@router.get("", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.scalars(select(UserModel).order_by(UserModel.id)).all()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(user_id, db)


@router.post("", response_model=UserOut, status_code=201)
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = UserModel(email=user.email, password=password_hash.hash(user.password))
    db.add(new_user)
    return commit_user(new_user, db)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    db_user = get_user_or_404(user_id, db)
    db_user.email = user.email
    db_user.password = password_hash.hash(user.password)
    return commit_user(db_user, db)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.delete(get_user_or_404(user_id, db))
    db.commit()
