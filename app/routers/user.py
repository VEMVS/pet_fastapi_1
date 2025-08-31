from .. import models, schemas, utils
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email = user.email.strip().lower()
    nickname = user.nickname.strip().lower()
    existing = (
        db.query(models.Users)
        .filter(
            (models.Users.email == user.email)
            | (models.Users.nickname == user.nickname)
        )
        .first()
    )
    if existing:
        if existing.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Этот адрес электронной почты уже используется",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Этот никнейм уже используется",
            )

    user_data = user.model_dump()
    user_data["email"] = email
    user_data["nickname"] = nickname
    user_data["password"] = utils.hash(user_data["password"])

    new_user = models.Users(**user_data)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
    "id": new_user.id,
    "email": new_user.email,
    "nickname": new_user.nickname,
    "created_at": new_user.created_at
}
    except IntegrityError:
        db.rollback()
        exists_email = (
            db.query(models.Users).filter(models.Users.email == user.email).first()
        )
        if exists_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такой адрес электронной почты уже занят",
            )
        exists_nick = (
            db.query(models.Users)
            .filter(models.Users.nickname == user.nickname)
            .first()
        )
        if exists_nick:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Такой никнейм уже занят"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось создать пользователя",
        )


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )
    return user


@router.get("/", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()
