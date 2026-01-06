from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr = 'sagar@example.com'
    password: str = 'asdasd'


class TokenResponse(BaseModel):
    access_token: str
    name: str
    email: EmailStr
    token_type: str = "bearer"
