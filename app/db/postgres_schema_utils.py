from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def get_table_schema(
    session: AsyncSession,
    table_name: str
) -> list[dict]:
    """
    Returns:
    [
      { "column_name": "col1", "data_type": "text" },
      ...
    ]
    """
    query = text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = :table_name
        ORDER BY ordinal_position
    """)

    result = await session.execute(
        query,
        {"table_name": table_name}
    )

    return [
        {
            "column_name": row.column_name,
            "data_type": row.data_type
        }
        for row in result.fetchall()
    ]

async def get_column_samples(
    session: AsyncSession,
    table_name: str,
    columns: list[str],
    limit: int = 5
) -> dict:
    """
    Returns:
    {
      "col1": ["a", "b"],
      "col2": ["10", "20"]
    }
    """
    samples = {}

    for col in columns:
        query = text(
            f'SELECT "{col}" FROM "{table_name}" '
            f'WHERE "{col}" IS NOT NULL '
            f'ORDER BY RANDOM() LIMIT :limit'
        )

        result = await session.execute(
            query,
            {"limit": limit}
        )

        samples[col] = [row[0] for row in result.fetchall()]

    return samples


async def get_random_records(
    session: AsyncSession,
    table_name: str,
    limit: int = 5
) -> list[dict]:
    query = text(
        f'SELECT * FROM "{table_name}" ORDER BY RANDOM() LIMIT :limit'
    )

    result = await session.execute(
        query,
        {"limit": limit}
    )

    rows = result.fetchall()
    columns = result.keys()

    return [
        dict(zip(columns, row))
        for row in rows
    ]
