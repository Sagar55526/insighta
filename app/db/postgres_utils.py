from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import pandas as pd
from bson import ObjectId


async def store_dataframe(
    session: AsyncSession,
    df: pd.DataFrame
) -> tuple[ObjectId, str]:
    object_id = ObjectId()
    table_name = f"{object_id}_tbl"

    # --- 1. Create table (quote column names safely)
    columns_ddl = ", ".join(
        f'"{col}" TEXT' for col in df.columns
    )

    await session.execute(
        text(f'CREATE TABLE "{table_name}" ({columns_ddl});')
    )

    # --- 2. Prepare INSERT (safe bind names)
    column_names = ", ".join(f'"{col}"' for col in df.columns)
    placeholders = ", ".join(f":col_{i}" for i in range(len(df.columns)))

    insert_query = text(
        f'INSERT INTO "{table_name}" ({column_names}) VALUES ({placeholders})'
    )

    # --- 3. Bulk values
    values = [
        {
            f"col_{i}": None if pd.isna(row[col]) else str(row[col])
            for i, col in enumerate(df.columns)
        }
        for _, row in df.iterrows()
    ]


    # --- 4. Execute bulk insert
    await session.execute(insert_query, values)
    await session.commit()

    return object_id, table_name
