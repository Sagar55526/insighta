from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class DBMapping(Document):
    user_id: str
    db_id: str
    table_name: str
    file_name: str

    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow
    )

    # schema-related fields
    schema: Optional[dict] = None
    schema_status: Optional[str] = "PENDING"
    schema_created_at: Optional[datetime] = None

    class Settings:
        name = "db_mapping"
