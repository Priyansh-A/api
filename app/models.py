from sqlmodel import SQLModel, Field
from typing import Union
from sqlalchemy import Column, Boolean, TIMESTAMP, text, String
from datetime import datetime
from pydantic import EmailStr
class Post(SQLModel, table=True):
    
    __tablename__ = "posts"
    
    id : int = Field(primary_key=True, nullable=False)
    title : str = Field(index= True, nullable=False)
    content : str = Field(index= True, nullable=False)
    published : bool = Field(default=True, sa_column=Column(Boolean, server_default='true', nullable=False))
    created_at : datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')))
    user_id: int | None = Field(default=None, foreign_key="users.id", ondelete="CASCADE", nullable=False)
    
class User(SQLModel, table=True):
    __tablename__ = "users"
    id : int = Field(primary_key=True, nullable=False)
    username: str = Field(index=True, nullable=False)
    email: EmailStr = Field(sa_column=Column("email", String, unique= True, nullable=False))
    password: str = Field(index=True, nullable=False)
    created_at : datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')))
    disabled: bool = Field(default=False, sa_column=Column(Boolean, server_default="false", nullable=False))