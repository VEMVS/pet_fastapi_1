from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, EmailStr


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок")
    content: str = Field(..., min_length=1, description="Текст")
    published: bool = Field(True, description="Публичен ли пост")

    model_config = {
        "from_attributes": True  
    }

    @field_validator("title", "content", mode="before")
    def _strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    published: Optional[bool] = None

    model_config = {"from_attributes": True}

    @field_validator("title", "content", mode="before")
    def _strip_if_present(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class PostResponse(PostBase):
    id: int
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True  
    }
