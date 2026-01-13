from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, DatabaseError
from datetime import date, datetime
from decimal import Decimal
from langchain_openai import ChatOpenAI
import json
import re


class ExecutorAgent:
    def __init__(
        self,
        max_rows: int | None = None,
        max_retries: int = 2,
    ):
        """
        max_rows:
            None  -> no limit applied
            int   -> optional post-fetch safeguard

        max_retries:
            Number of LLM-based SQL correction attempts
        """
        self.max_rows = max_rows
        self.max_retries = max_retries

        # 🔹 LLM used ONLY for syntax correction
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )

    # -------------------------------
    # Utils
    # -------------------------------
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
            raise ValueError("Unsafe SQL detected")

    async def _fix_sql_with_llm(self, sql: str, error: str, table_schema: dict) -> str:
        prompt = f"""
            You are a SQL expert.

            The following SQL query has a SYNTAX ERROR.
            Fix ONLY the syntax.
            Do NOT change table names, column names, or logic.

            Return ONLY the corrected SQL query.

            SQL QUERY:
            {sql}

            ERROR:
            {error}

            Table Schema:
            {table_schema}
            """
        response = await self.llm.ainvoke(prompt)

        fixed_sql = response.content.strip()

        # Remove markdown if present
        fixed_sql = re.sub(r"^```sql", "", fixed_sql)
        fixed_sql = re.sub(r"```$", "", fixed_sql)

        return fixed_sql.strip()
    

    async def run(
        self,
        sql: str,
        session: AsyncSession,
        table_schema=dict,
    ) -> dict:
        self._validate_sql(sql)

        attempt = 0
        last_error = None
        current_sql = sql

        while attempt <= self.max_retries:
            try:
                print(f"[ExecutorAgent] Attempt {attempt + 1}")
                print(f"[ExecutorAgent] SQL:\n{current_sql}")

                result = await session.execute(text(current_sql))

                rows = result.fetchall()
                columns = list(result.keys())

                if self.max_rows is not None and len(rows) > self.max_rows:
                    rows = rows[: self.max_rows]

                return {
                    "columns": columns,
                    "rows": [
                        [self._json_safe(value) for value in row]
                        for row in rows
                    ],
                    "row_count": len(rows),
                }

            except ProgrammingError as e:
                await session.rollback()
                last_error = str(e)

                if attempt >= self.max_retries:
                    break

                current_sql = await self._fix_sql_with_llm(
                    current_sql,
                    last_error,
                    table_schema,
                )
                attempt += 1

            except DatabaseError as e:
                last_error = str(e)
                break

        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "error": "Query could not be executed successfully after retries",
        }
