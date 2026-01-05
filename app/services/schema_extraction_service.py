from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres_schema_utils import (
    get_table_schema,
    get_random_records,
    get_column_samples,
)


async def extract_schema_payload(
    session: AsyncSession,
    table_name: str
) -> dict:
    schema = await get_table_schema(session, table_name)

    column_names = [col["column_name"] for col in schema]

    column_samples = await get_column_samples(
        session,
        table_name,
        column_names
    )

    random_records = await get_random_records(
        session,
        table_name
    )

    return {
        "table_name": table_name,
        "columns": [
            {
                "name": col["column_name"],
                "dtype": col["data_type"],
                "sample_values": column_samples.get(col["column_name"], [])
            }
            for col in schema
        ],
        "random_records": random_records
    }
