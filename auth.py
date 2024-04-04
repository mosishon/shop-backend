from fastapi.security import OAuth2PasswordBearer


import jwt
import bcrypt
from datetime import datetime, timedelta,UTC
from typing import Union
from config import settings
from pytz import timezone
# Secret key for encoding and decoding JWT tokens
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
oauth_user_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=settings.jwt_expire_after_minute)
    expire = datetime.now(timezone(settings.timezone)) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str) -> Union[dict, None]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None

# Function to create password hash
def create_password_hash(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Function to verify password hash
def verify_password_hash(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


