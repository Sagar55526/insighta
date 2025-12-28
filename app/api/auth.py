from fastapi import APIRouter, status

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_services import authenticate_user

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login_user(user: LoginRequest):
    return await authenticate_user(user)