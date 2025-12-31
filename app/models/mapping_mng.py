from datetime import datetime
from beanie import Document
from pydantic import Field
from bson import ObjectId

class DBMapping(Document):
    user_id: str
    db_id: str
    table_name: str
    file_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "db_mapping"