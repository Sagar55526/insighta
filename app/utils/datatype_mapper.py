import pandas as pd
import numpy as np
from typing import Dict

def map_pandas_to_postgres(dtype) -> str:
    """Map pandas dtype to PostgreSQL type"""
    
    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"
    
    elif pd.api.types.is_float_dtype(dtype):
        return "DOUBLE PRECISION"
    
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP"
    
    elif pd.api.types.is_datetime64_dtype(dtype):
        return "DATE"
    
    else:
        return "TEXT"


def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Infer PostgreSQL column types from DataFrame    
    Returns:
        Dictionary mapping column names to PostgreSQL types
    """
    column_types = {}
    
    for col in df.columns:
        dtype = df[col].dtype
        
        if dtype == 'object':
            try:
                numeric_col = pd.to_numeric(df[col], errors='coerce')
                non_null_count = numeric_col.notna().sum()
                
                if non_null_count / len(df) > 0.8:
                    if (numeric_col == numeric_col.astype(int)).all():
                        column_types[col] = "BIGINT"
                    else:
                        column_types[col] = "DOUBLE PRECISION"
                    continue
            except:
                pass
            
            try:
                datetime_col = pd.to_datetime(df[col], errors='coerce')
                non_null_count = datetime_col.notna().sum()
                
                if non_null_count / len(df) > 0.8:
                    column_types[col] = "TIMESTAMP"
                    continue
            except:
                pass
            
            column_types[col] = "TEXT"
        else:
            column_types[col] = map_pandas_to_postgres(dtype)
    
    return column_types