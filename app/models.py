from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy import Column, Boolean, TIMESTAMP, text, String
from datetime import datetime
from pydantic import EmailStr

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(
        sa_column=Column(
            String, 
            unique=True, 
            nullable=False,
            index=True
        )
    )
    password: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            TIMESTAMP(timezone=True), 
            nullable=False, 
            server_default=text('CURRENT_TIMESTAMP')
        )
    )
    disabled: bool = Field(
        default=False,
        sa_column=Column(
            Boolean, 
            nullable=False, 
            server_default=text('FALSE')
        )
    )
    posts: List["Post"] = Relationship(back_populates="owner")


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    content: str = Field(nullable=False) 
    published: bool = Field(
        default=True,
        sa_column=Column(
            Boolean, 
            nullable=False, 
            server_default=text('TRUE')
        )
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            TIMESTAMP(timezone=True), 
            nullable=False, 
            server_default=text('CURRENT_TIMESTAMP')
        )
    )
    user_id: int = Field(foreign_key="users.id", nullable=False)
    owner: Optional[User] = Relationship(back_populates="posts")


class Like(SQLModel, table=True):
    __tablename__ = "likes"
    
    user_id: int = Field(foreign_key="users.id", nullable=False, primary_key=True)
    post_id: int = Field(foreign_key="posts.id", nullable=False, primary_key=True)