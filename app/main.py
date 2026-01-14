from fastapi import FastAPI , Response, status, HTTPException, Depends, Query
from typing import Annotated
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlmodel import Session, select
import time
from . import models
from  .database import  create_db_and_tables, get_session
from contextlib import asynccontextmanager


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting")
    create_db_and_tables()
    yield
    print("application shutting down")


app = FastAPI(lifespan=lifespan)

# local db
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres', password='postgres123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


#all posts 
@app.get("/posts")
def get_posts(session: SessionDep) -> models.Post:
    posts = session.get(models.Post)
    # posts = session.exec(select(models.Post)).all()
    return {"data": posts}

# get specific post with given id
@app.get("/posts/{id}")
def get_post(id: int, session: SessionDep) -> models.Post:
    post = session.get(models.Post, id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"couldn't find a post with id: {id}")
    return {"message": post}

# delete a specific post
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    
    cursor.execute("""DELETE FROM posts where id = %s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    return  Response(status_code = status.HTTP_204_NO_CONTENT)

# add a post
@app.post("/posts", status_code = status.HTTP_201_CREATED) 
def create_posts(post: models.Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data": new_post}

# update details of a post
@app.put("/posts/{id}")
def update_post(id: int, post: models.Post):
    cursor.execute("""UPDATE posts SET title= %s, content= %s, published = %s where id= %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if  updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"couldn't find a post with id: {id}")
    return{"data": updated_post}


