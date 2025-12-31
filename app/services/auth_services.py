from fastapi import HTTPException, status

from app.models.user_pg import User
from app.schemas.auth import LoginRequest
from app.auth.security import verify_password, create_access_token

async def authenticate_user(data: LoginRequest) -> str:
    user = await User.find_one(User.email == data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token = create_access_token(subject=str(user.id))
    return {
        "access_token": access_token,
        "name": user.name,
        "email": user.email,
    }