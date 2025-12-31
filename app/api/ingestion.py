from fastapi import APIRouter, UploadFile, File, Depends
from app.auth.dependencies import get_current_user
from app.schemas.ingestion import IngestionResponse
from app.services.ingestion_service import ingest_files
from app.db.postgres import get_postgres_session
from app.models.user_pg import User

router =APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)

@router.post("/file", response_model=IngestionResponse)
async def upload_file(
    input_file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    pg_session=Depends(get_postgres_session)
):
    mapping = await ingest_files(
        input_file=input_file,
        user=current_user,
        pg_session=pg_session
    )

    return IngestionResponse(
        id=str(mapping.id), 
        object_id=str(mapping.id),
        table_name=mapping.table_name,
        file_name=mapping.file_name,
        created_at=mapping.created_at
    )