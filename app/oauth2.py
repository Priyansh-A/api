import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from .database import SessionDep
from . import schemas, models, config
from sqlmodel import select
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = config.settings.SECRET_KEY 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# creating token
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    
    
async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    query = select(models.User).where(models.User.id == token.id)
    val = await session.exec(query)
    user = val.first()
    return user