from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class IngestionResponse(BaseModel):
    mapping_id: str
    object_id: str
    table_name: str
    file_name: str
    created_at: datetime

class ColumnSchema(BaseModel):
    column_name: str
    inferred_type: str
    description: Optional[str] = None


class SchemaViewResponse(BaseModel):
    db_id: str
    file_name: str
    schema_status: str
    schema: List[ColumnSchema]


class SchemaUpdateRequest(BaseModel):
    db_id: str
    schema: List[ColumnSchema]