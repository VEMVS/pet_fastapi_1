from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict, field_serializer


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок")
    content: str = Field(..., min_length=1, description="Текст")
    published: bool = Field(False, description="Опубликован ли пост")
    model_config = {"from_attributes": True}

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


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserOutForPost(BaseModel):
    nickname: str
    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class PostResponse(PostBase):
    owner_id: int
    id: int
    created_at: datetime
    owner: UserOutForPost
    model_config = ConfigDict()

    @field_serializer('created_at')
    def format_created_at(self, v: datetime):
        return v.strftime("%d.%m.%y, %H:%M")
