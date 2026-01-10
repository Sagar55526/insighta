from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException, status
import re
import asyncio
from datetime import date, datetime
from decimal import Decimal
from app.db.postgres import AsyncSessionLocal

class ExecutorAgent:
    def __init__(self, max_rows: int | None = None):
        """
        max_rows:
            None  -> no limit applied, no enforcement
            int   -> optional safety cap (non-SQL, post-fetch)
        """
        self.max_rows = max_rows

    def _json_safe(self, value):
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        if isinstance(value, Decimal):
            return float(value)
        return value

    def _validate_sql(self, sql: str) -> None:
        if not sql or not sql.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty SQL query",
            )

        normalized = sql.strip().lower()

        blocked_keywords = {
            "insert",
            "update",
            "delete",
            "drop",
            "alter",
            "truncate",
            "create",
            "grant",
            "revoke",
        }

        if any(keyword in normalized for keyword in blocked_keywords):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unsafe SQL detected",
            )

    async def run(
        self,
        sql: str,
        session: AsyncSession,
    ) -> dict:
        self._validate_sql(sql)
        print(f"GENERATED SQL QUERY IS AS FOLLOWS: {sql}")
        result = await session.execute(text(sql))

        rows = result.fetchall()
        columns = list(result.keys())

        # Optional post-fetch safeguard (does NOT affect SQL)
        if self.max_rows is not None and len(rows) > self.max_rows:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Query returned {len(rows)} rows, exceeds max allowed {self.max_rows}",
            )
        print(f"EXECUTED RESULTS ARE AS FOLLOWS: {rows}")
        return {
            "columns": columns,
            "rows": [
                [self._json_safe(value) for value in row]
                for row in rows
            ],
            "row_count": len(rows),
        }

QUERY = """
SELECT
    "Risk_Level",
    COUNT(DISTINCT "Name") AS vendor_count
FROM tbl_695ff7b55645834edb877af3
GROUP BY "Risk_Level"
ORDER BY "Risk_Level"
"""


async def main():
    agent = ExecutorAgent(max_rows=None)

    async with AsyncSessionLocal() as session:
        result = await agent.run(QUERY, session)

        print("\nCOLUMNS:")
        print(result["columns"])

        print("\nROWS:")
        for row in result["rows"]:
            print(row)

        print("\nROW COUNT:")
        print(result["row_count"])


if __name__ == "__main__":
    asyncio.run(main())