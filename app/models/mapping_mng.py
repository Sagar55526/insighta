from datetime import datetime
from typing import Optional, List, Dict, Any
from beanie import Document
from pydantic import Field


class DBMapping(Document):
    user_id: str
    db_id: str
    table_name: str
    file_name: str
    
    column_types: Optional[Dict[str, str]] = None
    row_count: Optional[int] = None
    
    schema: Optional[List[Dict[str, Any]]] = None
    random_records: Optional[List[Dict[str, Any]]] = None
    schema_status: Optional[str] = "PENDING"
    schema_created_at: Optional[datetime] = None
    
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "db_mapping"