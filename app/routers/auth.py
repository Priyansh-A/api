from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..database import SessionDep
from .. import schemas, models, utils
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
    
    # token
    return {"token": "example token"}