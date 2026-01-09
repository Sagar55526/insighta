from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Any, Dict, List

class ThreadBase(BaseModel):
    title: str

class ThreadResponse(ThreadBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: str
    content: str
    is_bot: bool
    user_id: str
    thread_id: str
    created_at: datetime
    graphs: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes: True

class MessageCreate(BaseModel):
    content: str