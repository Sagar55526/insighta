from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True