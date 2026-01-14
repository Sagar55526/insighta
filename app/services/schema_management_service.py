from fastapi import HTTPException, status
from app.models.mapping_mng import DBMapping
from datetime import datetime


async def get_schema_for_user(
    user_id: str,
    db_id: str,
) -> DBMapping:
    mapping = await DBMapping.find_one(
        DBMapping.user_id == user_id,
        DBMapping.db_id == db_id,
    )

    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found",
        )

    if not mapping.schema:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Schema not generated yet",
        )

    return mapping


async def update_schema_descriptions(
    user_id: str,
    db_id: str,
    updated_schema: list[dict],
) -> DBMapping:
    mapping = await DBMapping.find_one(
        DBMapping.user_id == user_id,
        DBMapping.db_id == db_id,
    )

    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found",
        )
    
    if not mapping.schema:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Schema not found",
        )
        
    updates_by_column= {
        col["column_name"] : col.get("description")
        for col in updated_schema
    }

    merged_schema = []

    for col in mapping.schema:
        col_name = col["column_name"]
        merged_schema.append({
            "column_name": col_name,
            "inferred_type": col["inferred_type"],
            "description": updates_by_column.get(
                col_name,
                col.get("description"), 
            ),
        })
    mapping.schema = merged_schema
    mapping.schema_status = "USER_REFINED"
    mapping.updated_at = datetime.utcnow()

    await mapping.save()
    return mapping