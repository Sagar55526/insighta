from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

PROMPT_PATH = Path(__file__).parent / "prompts" / "response_agent.md"


class ResponseAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
        )

        self.prompt = PromptTemplate(
            template=PROMPT_PATH.read_text(),
            input_variables=["user_question", "sql_query", "columns", "rows", "row_count"]
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    async def run(
        self,
        sql_query: str,
        user_question: str,
        execution_result: dict,
    ) -> str:
        
        if not execution_result.get("success"):
            return "I encountered an error while querying the database. Please try rephrasing your question."
        
        results = execution_result.get("results", [])
        
        if not results:
            return "No results were returned from the database."
        
        if len(results) == 1:
            single_result = results[0]["result"]
            
            if not single_result.get("success"):
                return f"Query execution failed: {single_result.get('error', 'Unknown error')}"
            
            response = await self.chain.ainvoke({
                "user_question": user_question,
                "sql_query": results[0]["query"],
                "columns": json.dumps(single_result.get("columns", [])),
                "rows": json.dumps(single_result.get("rows", []), indent=2),
                "row_count": single_result.get("row_count", 0)
            })
            
            return response
        
        else:
            combined_results = []
            all_columns = []
            total_rows = 0
            
            for idx, result_item in enumerate(results, 1):
                if result_item["result"]["success"]:
                    result_data = result_item["result"]
                    combined_results.append({
                        "query_number": idx,
                        "query": result_item["query"],
                        "columns": result_data["columns"],
                        "rows": result_data["rows"],
                        "row_count": result_data["row_count"]
                    })
                    all_columns.extend(result_data["columns"])
                    total_rows += result_data["row_count"]
            
            if not combined_results:
                return "All queries failed to execute successfully."
            
            response = await self.chain.ainvoke({
                "user_question": user_question,
                "sql_query": f"Multiple queries executed ({len(combined_results)} queries)",
                "columns": json.dumps(list(set(all_columns))),
                "rows": json.dumps(combined_results, indent=2),
                "row_count": total_rows
            })
            
            return response