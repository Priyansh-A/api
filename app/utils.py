import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash(password: str):
    return password_hash(password)

def verify(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)
