from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def get_table_context(
        session: AsyncSession,
        table_name: str,
        sample_size: int = 5,
):
    columns_query = text(
        """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = :table_name
        """
    )

    columns = await session.execute(
        columns_query,
        {"table_name": table_name}
    )

    columns_info = [
        {"column": row[0], "dtype": row[1]}
        for row in columns.fetchall()
    ]

    sample_query = text(
        f'SELECT * FROM "{table_name}" LIMIT {sample_size}'
    )

    rows = await session.execute(sample_query)
    samples = rows.mappings().all()
    
    return {
        "columns": columns_info,
        "samples": samples
    }