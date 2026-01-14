from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.config import settings
from app.models.user import User

oauth2_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
) -> User:
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],  # MUST be a list
        )

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await User.get(user_id)

    if user is None:
        raise credentials_exception

    return user
