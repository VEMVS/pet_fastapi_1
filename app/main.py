from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import List
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# ---- GET: вернуть список постов ----
@app.get("/posts", response_model=List[schemas.PostResponse])
def test_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    find_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if find_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return find_post


# ---- POST: создать пост ----
@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.put("/posts/{post_id}", response_model=schemas.PostResponse)
def put_post(
    post_id: int, update_post: schemas.PostUpdate, db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} does not exist",
        )

    post_query.update(update_post.model_dump(), synchronize_session=False)
    db.commit()

    updatet_post = post_query.first()

    return updatet_post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_delete = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} does not exist",
        )

    db.delete(post_delete)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
