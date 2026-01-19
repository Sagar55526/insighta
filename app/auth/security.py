from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.ACCESS_TOKEN_EXPIRE_DAYS
        )

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )