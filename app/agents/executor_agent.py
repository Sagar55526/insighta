from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json
import re
from typing import Dict, Any, List

from app.agents.tools.query_executor_tool import QueryExecutorTool


PROMPT_PATH = Path(__file__).parent / "prompts" / "executor_agent.md"


class ExecutorAgent:
    def __init__(
        self,
        max_rows: int | None = None,
        max_retries: int = 2,
    ):
        self.max_rows = max_rows
        self.max_retries = max_retries
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )
        
        self.executor_tool = QueryExecutorTool(max_rows=max_rows)
        
        self._load_prompts()

    def _load_prompts(self):
        prompt_content = PROMPT_PATH.read_text()
        
        parts = prompt_content.split("---")
        
        if len(parts) >= 2:
            validator_part = parts[0].replace("## QUERY_VALIDATOR_PROMPT", "").strip()
            fixer_part = parts[1].replace("## QUERY_FIXER_PROMPT", "").strip()
        else:
            raise ValueError("Prompt file must contain both QUERY_VALIDATOR_PROMPT and QUERY_FIXER_PROMPT sections separated by ---")
        
        self.validator_template = validator_part
        self.fixer_template = fixer_part

    async def _validate_and_split_queries(
        self,
        sql: str,
        explanation: str,
        table_schema: dict
    ) -> Dict[str, Any]:
        
        prompt = self.validator_template.format(
            sql=sql,
            explanation=explanation,
            table_schema=json.dumps(table_schema, indent=2)
        )
        
        response = await self.llm.ainvoke(prompt)
        content = response.content.strip()
        
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'^```\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
        
        try:
            result = json.loads(content)
            return result
        except json.JSONDecodeError as e:
            print(f"[ExecutorAgent] Failed to parse LLM response: {e}")
            print(f"[ExecutorAgent] Raw response: {content}")
            queries = [q.strip() for q in sql.split(';') if q.strip()]
            return {
                "queries": queries if queries else [sql],
                "fixed": False,
                "changes_made": "Fallback: manual split"
            }

    async def _fix_query_syntax(
        self,
        sql: str,
        error: str,
        table_schema: dict
    ) -> str:
        
        prompt = self.fixer_template.format(
            sql=sql,
            error=error,
            table_schema=json.dumps(table_schema, indent=2)
        )
        
        response = await self.llm.ainvoke(prompt)
        fixed_sql = response.content.strip()
        
        fixed_sql = re.sub(r'^```sql\s*', '', fixed_sql)
        fixed_sql = re.sub(r'^```\s*', '', fixed_sql)
        fixed_sql = re.sub(r'\s*```$', '', fixed_sql)
        
        return fixed_sql.strip()

    async def _execute_with_retry(
        self,
        sql: str,
        session: AsyncSession,
        table_schema: dict,
        query_index: int = 0
    ) -> Dict[str, Any]:
        
        current_sql = sql
        
        for attempt in range(self.max_retries + 1):
            print(f"[ExecutorAgent] Query {query_index} - Attempt {attempt + 1}")
            
            result = await self.executor_tool.execute(current_sql, session)
            
            if result["success"]:
                return result
            
            if attempt < self.max_retries:
                print(f"[ExecutorAgent] Error: {result['error']}")
                print(f"[ExecutorAgent] Attempting to fix query...")
                
                current_sql = await self._fix_query_syntax(
                    current_sql,
                    result["error"],
                    table_schema
                )
                print(f"[ExecutorAgent] Fixed query: {current_sql}")
            else:
                print(f"[ExecutorAgent] Max retries reached for query {query_index}")
                return result
        
        return result

    async def run(
        self,
        sql: str,
        explanation: str,
        session: AsyncSession,
        table_schema: dict,
    ) -> Dict[str, Any]:
        
        print(f"\n{'='*80}")
        print(f"[ExecutorAgent] Starting execution")
        print(f"[ExecutorAgent] Input SQL: {sql}")
        print(f"[ExecutorAgent] Explanation: {explanation}")
        print(f"{'='*80}\n")
        
        validation_result = await self._validate_and_split_queries(
            sql, explanation, table_schema
        )
        
        queries = validation_result.get("queries", [])
        was_fixed = validation_result.get("fixed", False)
        changes = validation_result.get("changes_made", "none")
        
        if was_fixed:
            print(f"[ExecutorAgent] Queries were validated/fixed: {changes}")
        
        if not queries:
            return {
                "success": False,
                "results": [],
                "total_queries": 0,
                "successful_queries": 0,
                "error": "No valid queries found after validation"
            }
        
        print(f"[ExecutorAgent] Found {len(queries)} query(ies) to execute\n")
        
        results = []
        successful_count = 0
        
        for idx, query in enumerate(queries, 1):
            print(f"\n{'-'*80}")
            print(f"[ExecutorAgent] Processing Query {idx}/{len(queries)}")
            print(f"{'-'*80}")
            
            result = await self._execute_with_retry(
                query,
                session,
                table_schema,
                query_index=idx
            )
            
            if result["success"]:
                successful_count += 1
                print(f"[ExecutorAgent] ✅ Query {idx} executed successfully")
                print(f"[ExecutorAgent] Returned {result['row_count']} rows")
            else:
                print(f"[ExecutorAgent] ❌ Query {idx} failed: {result['error']}")
            
            results.append({
                "query_index": idx,
                "query": query,
                "result": result
            })
        
        print(f"\n{'='*80}")
        print(f"[ExecutorAgent] Execution complete")
        print(f"[ExecutorAgent] Total queries: {len(queries)}")
        print(f"[ExecutorAgent] Successful: {successful_count}")
        print(f"[ExecutorAgent] Failed: {len(queries) - successful_count}")
        print(f"{'='*80}\n")
        
        return {
            "success": successful_count > 0,
            "results": results,
            "total_queries": len(queries),
            "successful_queries": successful_count,
            "all_succeeded": successful_count == len(queries)
        }