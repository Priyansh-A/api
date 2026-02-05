from fastapi import FastAPI
from  .database import  engine
from contextlib import asynccontextmanager
from .routers import post, user, auth, like
from fastapi.middleware.cors import CORSMiddleware
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start connectiom
    async with engine.begin() as conn:
        await conn.run_sync(models.SQLModel.metadata.create_all)
    print("Database tables created")
    yield
    # shutdown
    await engine.dispose()
    print("Database connections closed")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}


