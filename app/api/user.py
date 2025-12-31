from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.user import UserCreate, UserResponse
from app.services.user_services import create_user
from app.models.user_pg import User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    created_user = await create_user(user)

    return UserResponse(
        id=str(created_user.id),
        name=created_user.name,
        email=created_user.email,
        is_active=created_user.is_active,
        created_at=created_user.created_at
    )

@router.get("/me")
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "is_active": current_user.is_active,
    }