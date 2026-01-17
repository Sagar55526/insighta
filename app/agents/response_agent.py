from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

PROMPT_PATH = Path(__file__).parent / "prompts" / "response_agent.md"


from typing import AsyncGenerator

class ResponseAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            streaming=True,
        )

        self.prompt = PromptTemplate(
            template=PROMPT_PATH.read_text(),
            input_variables=["user_question", "sql_query", "columns", "rows", "row_count"]
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    async def stream(
        self,
        sql_query: str,
        user_question: str,
        execution_result: dict,
    ) -> AsyncGenerator[str, None]:

        if not execution_result.get("success"):
            yield "I encountered an error while querying the database."
            return

        results = execution_result.get("results", [])
        if not results:
            yield "No results were returned from the database."
            return

        single_result = results[0]["result"]
        if not single_result.get("success"):
            yield f"Query execution failed: {single_result.get('error', 'Unknown error')}"
            return

        async for chunk in self.chain.astream({
            "user_question": user_question,
            "sql_query": results[0]["query"],
            "columns": json.dumps(single_result.get("columns", [])),
            "rows": json.dumps(single_result.get("rows", []), indent=2),
            "row_count": single_result.get("row_count", 0)
        }):
            yield chunk