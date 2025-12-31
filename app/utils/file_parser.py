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
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or corrupted file"
        )

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )

    return df
