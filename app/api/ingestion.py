from fastapi import APIRouter, UploadFile, File, Depends
from app.auth.dependencies import get_current_user
from app.schemas.ingestion import IngestionResponse
from app.services.ingestion_service import ingest_files
from app.db.postgres import get_postgres_session
from app.models.user_pg import User
from app.services.schema_service import generate_schema

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
        top_five_records=mapping.top_five_records,
        created_at=mapping.created_at
    )


@router.post("/{mapping_id}")
async def create_schema(
    mapping_id: str,
    pg_session=Depends(get_postgres_session)
):
    mapping = await generate_schema(mapping_id, pg_session)
    return {
        "status": "completed"
    }
