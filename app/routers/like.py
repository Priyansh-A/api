from fastapi import  Response, status, HTTPException, APIRouter, Depends
from sqlmodel import select
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, session: database.SessionDep, current_user:int = Depends(oauth2.get_current_user)):
    
    post = session.exec(select(models.Post).where(models.Post.id == like.post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {like.post_id} not found")
    like_query = session.exec(select(models.Like).where(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id))
    found_like = like_query.first()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user.username} has already liked the post {like.post_id}")
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        session.add(new_like)
        session.commit()
        return {"message": "Liked Successfully"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No like on the post")
        session.delete(found_like)
        session.commit()

        return {"message": "Unliked Successfully"}        