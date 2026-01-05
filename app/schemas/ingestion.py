from pydantic import BaseModel
from datetime import datetime

class IngestionResponse(BaseModel):
    mapping_id: str
    object_id: str
    table_name: str
    file_name: str
    created_at: datetime
