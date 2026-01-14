from fastapi import FastAPI , Response, status, HTTPException, Depends, Query
from typing import Annotated
from sqlmodel import Session, select
import time
from .models import Post, User
from datetime import datetime
from . import schemas
from  .database import  create_db_and_tables, get_session
from contextlib import asynccontextmanager
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash



SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting")
    create_db_and_tables()
    yield
    print("application shutting down")


app = FastAPI(lifespan=lifespan)

#all posts 
@app.get("/posts")
def get_posts(session: SessionDep) -> list[Post]:
    posts = session.exec(select(Post)).all()
    return posts

# get specific post with given id
@app.get("/posts/{id}")
def get_post(id: int, session: SessionDep) -> Post:
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"couldn't find a post with id: {id}")
    return  post

# delete a specific post
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, session: SessionDep):
    deleted_post = session.get(Post, id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    session.delete(deleted_post)
    session.commit()
    return  Response(status_code = status.HTTP_204_NO_CONTENT)

# add a post
@app.post("/posts", status_code = status.HTTP_201_CREATED) 
def create_posts(post: Post, session : SessionDep)-> Post:
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

# update details of a post
@app.put("/posts/{id}", response_model=schemas.UpdatePost)
def update_post(id: int, post_update: schemas.UpdatePost,session: SessionDep)-> Post:
    db_post = session.get(Post, id)
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"couldn't find a post with id: {id}")
    update_post = post_update.model_dump(exclude_unset=True)
    for field, value in update_post.items():
        setattr(db_post, field, value)
    db_post.created_at = datetime.now()
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: User , session : SessionDep)-> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

