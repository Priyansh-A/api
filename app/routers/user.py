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
def create_user(user: schemas.UserCreate , session : SessionDep)-> User:
    
    # hash password
    hashed_password = utils.password_hash.hash(user.password)
    user.password = hashed_password
    
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int, session: SessionDep):
    user = session.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id: {id} does not exist")
    return user


