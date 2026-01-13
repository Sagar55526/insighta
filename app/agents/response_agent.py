from pathlib import Path
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


PROMPT_PATH = Path(__file__).parent / "prompts" / "response_agent.md"


class ResponseAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            verbose=True,
        )

        self.prompt = PromptTemplate(
            template=PROMPT_PATH.read_text(),
            input_variables=["user_question", "sql_query", "columns", "rows", "row_count"],
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    async def run(
        self,
        user_question: str,
        sql_query: str,
        execution_result: dict,
    ) -> dict:
        print(f"Response Agent Input:")
        print(f"  Question: {user_question}")
        print(f"  Rows: {execution_result['rows']}")
        print(f"  Row Count: {execution_result['row_count']}")

        response_text = await self.chain.ainvoke(
            {
                "user_question": user_question,
                "sql_query": sql_query,
                "columns": json.dumps(execution_result["columns"]),
                "rows": json.dumps(execution_result["rows"]),
                "row_count": execution_result["row_count"],
            }
        )
        
        print(f"Response Agent Output:\n{response_text}")
        return response_text.strip()