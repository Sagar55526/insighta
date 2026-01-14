from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, DatabaseError
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, Any, List


class QueryExecutorTool:
    def __init__(self, max_rows: int | None = None):
        self.max_rows = max_rows

    def _json_safe(self, value):
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        if isinstance(value, Decimal):
            return float(value)
        return value

    def _validate_sql(self, sql: str) -> None:
        if not sql or not sql.strip():
            raise ValueError("Empty SQL query")

        normalized = sql.strip().lower()

        blocked_keywords = {
            "insert", "update", "delete", "drop",
            "alter", "truncate", "create", "grant", "revoke"
        }

        if any(keyword in normalized for keyword in blocked_keywords):
            raise ValueError(f"Unsafe SQL detected: contains blocked keyword")

    async def execute(
        self,
        sql: str,
        session: AsyncSession,
    ) -> Dict[str, Any]:
        try:
            self._validate_sql(sql)

            print(f"[QueryExecutorTool] Executing: {sql[:150]}...")

            result = await session.execute(text(sql))
            rows = result.fetchall()
            columns = list(result.keys())

            if self.max_rows is not None and len(rows) > self.max_rows:
                rows = rows[:self.max_rows]

            return {
                "success": True,
                "columns": columns,
                "rows": [
                    [self._json_safe(value) for value in row]
                    for row in rows
                ],
                "row_count": len(rows),
                "error": None
            }

        except (ProgrammingError, DatabaseError) as e:
            await session.rollback()
            return {
                "success": False,
                "columns": [],
                "rows": [],
                "row_count": 0,
                "error": str(e)
            }
        except Exception as e:
            await session.rollback()
            return {
                "success": False,
                "columns": [],
                "rows": [],
                "row_count": 0,
                "error": f"Unexpected error: {str(e)}"
            }