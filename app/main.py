from fastapi import FastAPI
from  .database import  create_db_and_tables
from contextlib import asynccontextmanager
from .routers import post, user, auth, like


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting")
    create_db_and_tables()
    yield
    print("application shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}


