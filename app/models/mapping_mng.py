from datetime import datetime
from beanie import Document
from pydantic import Field
from bson import ObjectId
from typing import List


class ColumnSchema(Document):
    column_name: str
    dtype: str
    description: str
    sample_data: list[str]

class DBMapping(Document):
    user_id: str
    db_id: str
    table_name: str
    file_name: str
    schema: List[ColumnSchema]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "db_mapping"