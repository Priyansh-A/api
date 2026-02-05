from .. import schemas, oauth2
from ..models import Post, Like
from fastapi import  Response, status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import selectinload
from sqlmodel import select, func
from ..database import SessionDep
from datetime import datetime
from typing import List, Optional
#all posts 

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# getting all posts
# response model gives the output in the form of that model
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    session: SessionDep,
    current_user: int = Depends(oauth2.get_current_user), 
    limit: int = 5, 
    skip: int = 0, 
    search: Optional[str] = ""
):
    # Query to get posts with like counts
    query = (
        select(Post,func.count(Like.post_id).label("likes")).join(Like, Like.post_id == Post.id, isouter=True).group_by(Post.id).options(selectinload(Post.owner)))
    if search:
        query = query.where(Post.title.contains(search))
    
    query = query.limit(limit).offset(skip)
    
    result = await session.exec(query)
    results = result.all()
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Couldn't find any posts"
        )
    
    return results

# get specific post with given id
@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    query = select(Post, id, func.count(Like.post_id).label("likes")).join(Like, Like.post_id == Post.id, isouter=True).group_by(Post.id).options(selectinload(Post.owner)).where(id == Post.id)
    result = await session.exec(query)
    post = result.first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"couldn't find a post with id: {id}")
    return post

# delete a specific post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_posts(
    id: int,
    session: SessionDep,
    current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = await session.get(Post, id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    if deleted_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="post doesn't belong to the current user")
    await session.delete(deleted_post)
    await session.commit()
    return  Response(status_code = status.HTTP_204_NO_CONTENT)

# add a post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PostUser) 
async def create_posts(post: Post,
                session : SessionDep, 
                current_user: int = Depends(oauth2.get_current_user)):
    
    post.user_id = current_user.id
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

# update details of a post
@router.put("/{id}", response_model=schemas.UpdatePost)
async def update_post(id: int, 
                post_update: schemas.UpdatePost,
                session: SessionDep, 
                current_user: int = Depends(oauth2.get_current_user)):
    db_post = await session.get(Post, id)
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"couldn't find a post with id: {id}")
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="post doesn't belong to the current user")
    update_post = post_update.model_dump(exclude_unset=True)
    for field, value in update_post.items():
        setattr(db_post, field, value)
    db_post.created_at = datetime.now()
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post
