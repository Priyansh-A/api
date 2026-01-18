from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends 
postgres_database_url = f"postgresql://postgres:postgres123@localhost/fastapi"
engine = create_engine(postgres_database_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("db table created")

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
            
SessionDep = Annotated[Session, Depends(get_session)]
