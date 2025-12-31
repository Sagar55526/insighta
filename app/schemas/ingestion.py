from pydantic import BaseModel
from datetime import datetime

class IngestionResponse(BaseModel):
    id: str
    table_name: str
    file_name: str
    created_at: datetime
