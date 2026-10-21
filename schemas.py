from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class Post(BaseModel):
    title: str
    content: str


class PostOut(Post):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class User(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime
