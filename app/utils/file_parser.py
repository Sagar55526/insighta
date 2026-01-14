import pandas as pd
from fastapi import UploadFile, HTTPException, status

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}


async def parse_file(file: UploadFile) -> pd.DataFrame:
    extension = file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV and Excel files are supported"
        )

    try:
        if extension == "csv":
            df = pd.read_csv(file.file, parse_dates=True)
            
            df = df.infer_objects()
            
        else:
            df = pd.read_excel(file.file)
            df = df.infer_objects()
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupted file: {str(e)}"
        )

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )
    df.columns = df.columns.str.strip().str.replace(r'[^\w\s]', '_', regex=True).str.replace(r'\s+', '_', regex=True)

    return df