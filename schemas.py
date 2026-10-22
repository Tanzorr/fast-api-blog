from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Pagination(BaseModel):
    limit: int
    offset: int


class PostFilters(BaseModel):
    """Query parameters of `GET /posts`. Every filter is optional."""

    search: str | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    min_likes: int | None = Field(default=None, ge=0)


class Post(BaseModel):
    title: str
    content: str


class PostOut(Post):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    likes_count: int


class User(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
