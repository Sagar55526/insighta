# app/db/postgres_utils.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import pandas as pd
from bson import ObjectId
from app.utils.datatype_mapper import infer_column_types


async def store_dataframe(
    session: AsyncSession,
    df: pd.DataFrame
) -> tuple[ObjectId, str]:
    object_id = ObjectId()
    table_name = f"tbl_{object_id}"  # Prefix with 'tbl_' for clarity

    # --- 1. Infer column types
    column_types = infer_column_types(df)

    # --- 2. Create table with proper types
    columns_ddl = ", ".join(
        f'"{col}" {column_types[col]}' for col in df.columns
    )

    create_table_query = f'CREATE TABLE "{table_name}" ({columns_ddl});'
    
    await session.execute(text(create_table_query))

    # --- 3. Convert DataFrame columns to appropriate types
    df_converted = df.copy()
    
    for col in df.columns:
        pg_type = column_types[col]
        
        if pg_type == "BIGINT":
            df_converted[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        
        elif pg_type == "DOUBLE PRECISION":
            df_converted[col] = pd.to_numeric(df[col], errors='coerce')
        
        elif pg_type == "BOOLEAN":
            df_converted[col] = df[col].astype('boolean')
        
        elif pg_type == "TIMESTAMP":
            df_converted[col] = pd.to_datetime(df[col], errors='coerce')
        
        elif pg_type == "TEXT":
            # Keep as is, but handle NaN
            df_converted[col] = df[col].astype(str).replace('nan', None)

    # --- 4. Prepare INSERT with proper type handling
    column_names = ", ".join(f'"{col}"' for col in df_converted.columns)
    placeholders = ", ".join(f":col_{i}" for i in range(len(df_converted.columns)))

    insert_query = text(
        f'INSERT INTO "{table_name}" ({column_names}) VALUES ({placeholders})'
    )

    # --- 5. Prepare values with proper type handling
    values = []
    for _, row in df_converted.iterrows():
        row_dict = {}
        for i, col in enumerate(df_converted.columns):
            value = row[col]
            
            # Handle pandas NA/NaN/NaT
            if pd.isna(value):
                row_dict[f"col_{i}"] = None
            elif isinstance(value, pd.Timestamp):
                row_dict[f"col_{i}"] = value.to_pydatetime()
            else:
                row_dict[f"col_{i}"] = value
        
        values.append(row_dict)

    # --- 6. Execute bulk insert
    if values:  # Only insert if we have data
        await session.execute(insert_query, values)
    
    await session.commit()

    return object_id, table_name