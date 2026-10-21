from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import PostModel
from schemas import Post, PostOut

router = APIRouter(prefix="/posts", tags=["posts"])


def get_post_or_404(post_id: int, db: Session) -> PostModel:
    post = db.get(PostModel, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    return post


@router.get("", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.scalars(select(PostModel).order_by(PostModel.id)).all()


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
