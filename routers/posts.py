from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import Select, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user, get_pagination
from models import PostModel, UserModel
from schemas import Pagination, Post, PostFilters, PostOut

router = APIRouter(prefix="/posts", tags=["posts"])


def get_post_or_404(post_id: int, db: Session) -> PostModel:
    post = db.get(PostModel, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    return post


def filter_posts(query: Select, filters: PostFilters) -> Select:
    """Add one WHERE condition for each filter the client sent."""
    if filters.search is not None:
        # autoescape: "%" and "_" in the search are plain characters, not wildcards.
        query = query.where(
            or_(
                PostModel.title.icontains(filters.search, autoescape=True),
                PostModel.content.icontains(filters.search, autoescape=True),
            )
        )
    if filters.created_after is not None:
        query = query.where(PostModel.created_at >= filters.created_after)
    if filters.created_before is not None:
        query = query.where(PostModel.created_at <= filters.created_before)
    if filters.min_likes is not None:
        query = query.where(PostModel.likes_count >= filters.min_likes)
    return query


@router.get("", response_model=list[PostOut])
def get_posts(
    filters: Annotated[PostFilters, Query()],
    pagination: Pagination = Depends(get_pagination),
    db: Session = Depends(get_db),
):
    query = filter_posts(select(PostModel), filters)
    # Order by id, so two pages never show the same Post.
    query = query.order_by(PostModel.id)
    query = query.limit(pagination.limit).offset(pagination.offset)
    return db.scalars(query).all()


@router.post("", response_model=PostOut, status_code=201)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = PostModel(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: Post, db: Session = Depends(get_db)):
    db_post = get_post_or_404(post_id, db)
    for field, value in post.model_dump().items():
        setattr(db_post, field, value)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db.delete(get_post_or_404(post_id, db))
    db.commit()


@router.post("/{post_id}/likes", response_model=PostOut, status_code=201)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    post = get_post_or_404(post_id, db)
    post.liked_by.append(current_user)
    # The primary key (user_id, post_id) stops a second like (I-6, ADR-007).
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail=f"You already like Post {post_id}"
        ) from None
    db.refresh(post)
    return post


@router.delete("/{post_id}/likes", status_code=204)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    post = get_post_or_404(post_id, db)
    if current_user not in post.liked_by:
        raise HTTPException(status_code=404, detail=f"You do not like Post {post_id}")
    post.liked_by.remove(current_user)
    db.commit()
