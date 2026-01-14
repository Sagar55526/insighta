from app.models.mapping_mng import DBMapping
from app.utils.file_parser import parse_file
from app.db.postgres_utils import store_dataframe
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

async def ingest_files(
    input_file: UploadFile,
    user: User,
    pg_session: AsyncSession,
):
    
    df = await parse_file(input_file)

    object_id, tbl_name = await store_dataframe(pg_session, df)

    mapping = DBMapping(
        user_id=str(user.id),
        db_id=str(object_id),
        table_name=tbl_name,
        file_name=input_file.filename
    )
    await mapping.insert()
    return mapping