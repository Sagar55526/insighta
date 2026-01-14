from datetime import datetime
from typing_extensions import Annotated
from beanie import Document, Indexed
from pydantic import EmailStr, Field

class User(Document):
    name: str = Field(..., min_length=2)
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"      # MongoDB collection name