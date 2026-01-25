from fastapi import APIRouter, UploadFile, File, Depends
from datetime import datetime
from app.auth.dependencies import get_current_user
from app.schemas.ingestion import IngestionResponse, SchemaViewResponse, SchemaUpdateRequest
from app.services.ingestion_service import ingest_files
from app.db.postgres import get_postgres_session
from app.models.user import User
from app.services.schema_extraction_service import extract_schema_payload
from app.services.schema_maker_service import generate_and_store_schema
from app.services.schema_management_service import get_schema_for_user, update_schema_descriptions
from app.services.message_service import get_db_id

router =APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)

@router.post("/file", response_model=IngestionResponse)
async def upload_file(
    input_file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    pg_session=Depends(get_postgres_session),
):
    mapping = await ingest_files(
        input_file=input_file,
        user=current_user,
        pg_session=pg_session
    )

    schema_payload = await extract_schema_payload(
        pg_session,
        mapping.table_name
    )

    await generate_and_store_schema(
        mapping=mapping,
        schema_payload=schema_payload
    )

    return IngestionResponse(
        mapping_id=str(mapping.id),   
        object_id=mapping.db_id,         
        table_name=mapping.table_name,
        file_name=mapping.file_name,
        created_at=datetime.utcnow() 
    )


@router.get(
    "",
    response_model=SchemaViewResponse,
)
async def view_schema(
    current_user=Depends(get_current_user),
):
    db_id = await get_db_id(current_user.id)
    mapping = await get_schema_for_user(
        user_id=str(current_user.id),
        db_id=db_id,
    )

    return SchemaViewResponse(
        db_id=mapping.db_id,
        table_name=mapping.table_name,
        file_name=mapping.file_name,
        schema_status=mapping.schema_status,
        schema=mapping.schema,
    )

@router.put(
    "",
    response_model=SchemaViewResponse,
)
async def update_schema(
    payload: SchemaUpdateRequest,
    current_user=Depends(get_current_user),
):
    db_id = await get_db_id(current_user.id)
    mapping = await update_schema_descriptions(
        user_id=str(current_user.id),
        db_id=db_id,
        updated_schema=[col.dict() for col in payload.schema],
    )

    return SchemaViewResponse(
        db_id=mapping.db_id,
        table_name=mapping.table_name,
        file_name=mapping.file_name,
        schema_status=mapping.schema_status,
        schema=mapping.schema,
    )
