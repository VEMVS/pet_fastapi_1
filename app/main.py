from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel, Field, conint
from typing import Optional, List, Dict, Any, Annotated
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from database import engine, SessionLocal
from sqlalchemy import inspect
from sqlalchemy.orm import Session



inspector = inspect(engine)
if "users" not in inspector.get_table_names():
    print("Таблица 'users' не найдена — создаю её")
    from models import Base

    Base.metadata.create_all(bind=engine)
else:
    print("Таблица 'users' уже есть — пропускаю создание")


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    
class Post(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    published: bool = True


DB_USER = "postgres"
DB_PASSWORD = "18491256"
DB_HOST = "172.17.128.1"
DB_PORT = "5432"
DB_NAME = "fastapi"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Database connection was succesfull!")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ", error)


@app.get("/posts/")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)

    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with: {id} was not found",
        )

    return {"Post_deatail": post}


@app.post("/posts/")
def create_posts(post: Post):
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title})")

    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
                   RETURNING *""",
        (post.title, post.content, post.published),
    )

    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s returning *""",
        (str(id)),
    )
    delete_post = cursor.fetchone()

    if delete_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with: {id} was not found",
        )
    conn.commit()

    return {"delete_post": delete_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s 
                   WHERE id = %s returning *""",
        (post.title, post.content, post.published, str(id)),
    )
    update_post = cursor.fetchone()
    conn.commit()

    if update_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with: {id} does not exist",
        )

    return {"Post_update": update_post}
