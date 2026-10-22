from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Table, Text, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from database import Base

# Many-to-many: one row = one User likes one Post. The two columns together are
# the primary key, so a User can like a Post only once (I-6).
post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
)


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    liked_by: Mapped[list["UserModel"]] = relationship(
        secondary=post_likes, back_populates="liked_posts"
    )
    # A subquery inside the SELECT of the Post, so a list of Posts and their
    # counts is one query (ADR-014).
    likes_count: Mapped[int] = column_property(
        select(func.count())
        .where(post_likes.c.post_id == id)
        .correlate_except(post_likes)
        .scalar_subquery()
    )


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    liked_posts: Mapped[list[PostModel]] = relationship(
        secondary=post_likes, back_populates="liked_by", order_by=PostModel.id
    )
