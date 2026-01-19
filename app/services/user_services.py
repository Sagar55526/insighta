from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.auth.security import hash_password
from app.models.user import User
from app.models.chat import Thread
from app.schemas.user import UserCreate

async def create_user(user_data: UserCreate) -> User:
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            detail="Invalid EmailId!!!",
            status_code=status.HTTP_409_CONFLICT
        )
    user = User(
        name = user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )
    await user.insert()
    try:
        default_thread = Thread(
            title="default",
            user_id=str(user.id),
        )
        await default_thread.insert()
    except Exception as e:
        print("⚠️ Failed to create default thread:", e)
    return user