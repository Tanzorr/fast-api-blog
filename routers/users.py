from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user, get_pagination
from models import UserModel
from schemas import Pagination, PostOut, User, UserOut
from security import password_hash

router = APIRouter(prefix="/users", tags=["users"])


def get_user_or_404(user_id: int, db: Session) -> UserModel:
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


def get_own_user_or_403(
    user_id: int, current_user: UserModel, db: Session
) -> UserModel:
    # 404 first: a missing User is "not found", not "forbidden".
    user = get_user_or_404(user_id, db)
    if user.id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can change only your own account"
        )
    return user


def commit_user(user: UserModel, db: Session) -> UserModel:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail=f"Email {user.email} is already registered"
        ) from None
    db.refresh(user)
    return user


@router.get("", response_model=list[UserOut])
def get_users(
    pagination: Pagination = Depends(get_pagination), db: Session = Depends(get_db)
):
    query = (
        select(UserModel)
        .order_by(UserModel.id)
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    return db.scalars(query).all()


# Must stay before "/{user_id}", or FastAPI reads "me" as an id and returns 422.
@router.get("/me", response_model=UserOut)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.get("/me/likes", response_model=list[PostOut])
def get_my_likes(current_user: UserModel = Depends(get_current_user)):
    return current_user.liked_posts


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(user_id, db)


@router.post("", response_model=UserOut, status_code=201)
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = UserModel(email=user.email, password=password_hash.hash(user.password))
    db.add(new_user)
    return commit_user(new_user, db)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: User,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_user = get_own_user_or_403(user_id, current_user, db)
    db_user.email = user.email
    db_user.password = password_hash.hash(user.password)
    return commit_user(db_user, db)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db.delete(get_own_user_or_403(user_id, current_user, db))
    db.commit()
