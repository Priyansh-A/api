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

