from fastapi import FastAPI
from  .database import  create_db_and_tables
from contextlib import asynccontextmanager
from .routers import post, user, auth, like
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting")
    create_db_and_tables()
    yield
    print("application shutting down")


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
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


