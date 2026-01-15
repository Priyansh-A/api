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
    pass

class User(BaseModel):
    email : EmailStr
    password: str
    username: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str
    
