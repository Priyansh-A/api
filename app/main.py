from fastapi import FastAPI
from  .database import  create_db_and_tables
from contextlib import asynccontextmanager
import os
from pathlib import Path
from dotenv import load_dotenv
from .routers import post, user


# env files
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting")
    create_db_and_tables()
    yield
    print("application shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}


