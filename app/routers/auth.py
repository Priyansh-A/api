from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..database import SessionDep
from .. import schemas, models, utils, oauth2
from sqlmodel import select


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: schemas.UserLogin ,session: SessionDep):
    user =  session.exec(select(models.User).where(models.User.username == user_credentials.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # compare passwords
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")    
    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "username": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}