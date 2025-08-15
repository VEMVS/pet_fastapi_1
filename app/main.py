from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import List
from . import models, schemas, utils
from .database import get_db
from sqlalchemy.orm import Session
from .routers import post, user

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)



