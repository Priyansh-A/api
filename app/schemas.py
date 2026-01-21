from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class UpdatePost(PostBase):
    created_at: datetime = Field(
        default_factory = datetime.now
    )
    
    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True

class PostUser(BaseModel):
    user_id: int
    id: int

class User(BaseModel):
    email : EmailStr
    password: str
    username: str
    disabled: bool    

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    
class UserLogin(BaseModel):
    username: str
    password: str    

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None