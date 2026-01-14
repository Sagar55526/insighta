from beanie import Document
from typing import Optional, List
from datetime import datetime
from pydantic import Field

class Message(Document):
    content: str
    user: str
    thread_id: str
    is_bot: bool
    graphs: Optional[List[dict]] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "messages"

class Thread(Document):
    title: str = Field(..., min_length=1)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "threads" 