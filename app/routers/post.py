from .. import schemas, oauth2
from ..models import Post
from fastapi import  Response, status, HTTPException, APIRouter, Depends
from sqlmodel import select
from ..database import SessionDep
from datetime import datetime
#all posts 

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/")
def get_posts(session: SessionDep) -> list[Post]:
    posts = session.exec(select(Post)).all()
    return posts

# get specific post with given id
@router.get("/{id}")
def get_post(id: int, session: SessionDep) -> Post:
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"couldn't find a post with id: {id}")
    return  post

# delete a specific post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, session: SessionDep,user_id: int = Depends(oauth2.get_current_user)):
    deleted_post = session.get(Post, id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    session.delete(deleted_post)
    session.commit()
    return  Response(status_code = status.HTTP_204_NO_CONTENT)

# add a post
@router.post("/", status_code = status.HTTP_201_CREATED) 
def create_posts(post: Post, session : SessionDep, user_id: int = Depends(oauth2.get_current_user)):
    
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

# update details of a post
@router.put("/{id}", response_model=schemas.UpdatePost)
def update_post(id: int, post_update: schemas.UpdatePost,session: SessionDep,user_id: int = Depends(oauth2.get_current_user)):
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
