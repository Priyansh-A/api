from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Boolean, TIMESTAMP, text
from datetime import datetime
class Post(SQLModel, table=True):
    
    __tablename__ = "posts"
    
    id : int = Field(primary_key=True, nullable=False)
    title : str = Field(index= True, nullable=False)
    content : str = Field(index= True, nullable=False)
    published : bool = Field(default=True, sa_column=Column(Boolean, server_default='true', nullable=False))
    created_at : datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')))