from passlib.context import CryptContext
import hashlib
from datetime import datetime, timedelta, UTC
from jose import jwt 
from core.config import Settings



pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)



def hash_password(password: str) -> str:

    return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)



ALGORITHM = "HS256"
def create_acess_token(user_id : int) -> str:

    expire = datetime.now(UTC) + timedelta(minutes= Settings.ACESS_TOKEN_EXPIRE)

    payload = {
        'sub' : str(user_id),
        'exp' : expire,
        'type': "acess"
    }

    return jwt.encode(payload, Settings.SECRET_KEY, algorithm= ALGORITHM)



def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        Settings.SECRET_KEY,
        algorithms=[ALGORITHM]
    )