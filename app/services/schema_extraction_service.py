from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, inspect
import json


async def extract_schema_payload(
    pg_session: AsyncSession,
    table_name: str,
    sample_size: int = 5
) -> dict:
    
    result = await pg_session.execute(
        text(f'SELECT column_name, data_type FROM information_schema.columns WHERE table_name = :tbl'),
        {"tbl": table_name}
    )
    columns_info = result.fetchall()

    columns = []
    for col_name, col_type in columns_info:
        sample_result = await pg_session.execute(
            text(f'SELECT DISTINCT "{col_name}" FROM "{table_name}" WHERE "{col_name}" IS NOT NULL LIMIT 5')
        )
        sample_values = [str(row[0]) for row in sample_result.fetchall()]

        columns.append({
            "name": col_name,
            "dtype": col_type,
            "sample_values": sample_values
        })

    random_result = await pg_session.execute(
        text(f'SELECT * FROM "{table_name}" ORDER BY RANDOM() LIMIT :limit'),
        {"limit": sample_size}
    )
    
    rows = random_result.fetchall()
    column_names = [col_name for col_name, _ in columns_info]
    
    random_records = [
        {column_names[i]: (None if val is None else str(val)) for i, val in enumerate(row)}
        for row in rows
    ]

    return {
        "table_name": table_name,
        "columns": columns,
        "random_records": random_records
    }