from .. import schemas, utils
from ..models import User
from fastapi import status, HTTPException,  APIRouter
from sqlmodel import select
from ..database import SessionDep

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate , session : SessionDep):
    
    # hash password
    hashed_password = utils.password_hash.hash(user.password)
    user.password = hashed_password
    
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schemas.UserOut)
async def get_user(id: int, session: SessionDep):
    
    query = select(User).where(User.id == id)
    result = await session.exec(query)
    user = result.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user


