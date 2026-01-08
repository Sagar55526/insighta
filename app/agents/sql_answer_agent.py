# app/agents/sql_answer_agent.py
from pathlib import Path
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import re

PROMPT_PATH = Path(__file__).parent / "prompts" / "sql_answer_agent.md"


class SQLAnswerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )

        self.prompt = PromptTemplate(
            template=PROMPT_PATH.read_text(),
            input_variables=["table_name", "schema", "user_question"],
        )

        self.chain = self.prompt | self.llm | JsonOutputParser()

    async def run(
        self,
        table_name: str,
        table_schema: dict,
        user_question: str,
    ) -> dict:
        
        schema_list = table_schema.get("schema", [])
        
        response = await self.chain.ainvoke({
            "table_name": table_name,
            "schema": json.dumps(schema_list, indent=2),
            "user_question": user_question
        })

        validated_response = self._validate_response(response, table_name, schema_list)
        
        return validated_response

    def _validate_response(self, response: dict, table_name: str, schema: list) -> dict:
        if not isinstance(response, dict):
            response_str = str(response)
            response_str = re.sub(r'^```json\s*', '', response_str)
            response_str = re.sub(r'\s*```$', '', response_str)
            response = json.loads(response_str)

        sql = response.get("sql")
        explanation = response.get("explanation", "")

        if sql:
            if table_name not in sql:
                raise ValueError(f"Generated SQL does not use the correct table name: {table_name}")

            column_names = [col["column_name"] for col in schema]
            for col_name in column_names:
                if col_name.lower() in sql.lower() and f'"{col_name}"' not in sql:
                    sql = sql.replace(col_name, f'"{col_name}"')

        return {
            "sql": sql,
            "explanation": explanation
        }
    
# app/agents/sql_answer_agent.py (test section)

if __name__ == "__main__":
    import asyncio

    async def main():
        agent = SQLAnswerAgent()

        test_schema = {
            "schema": [
                {
                    "column_name": "Monthly_Spend",
                    "inferred_type": "string",
                    "sample_values": ["69727", "9842", "65087", "202534", "8073"],
                    "description": "Monthly spending amount"
                },
                {
                    "column_name": "Sites",
                    "inferred_type": "string",
                    "sample_values": ["169", "22", "11", "9", "15"],
                    "description": "Number of sites involved"
                },
                {
                    "column_name": "Outstanding",
                    "inferred_type": "string",
                    "sample_values": ["522000", "2985041", "170451", "660489", "251141"],
                    "description": "Outstanding amount"
                },
                {
                    "column_name": "Days",
                    "inferred_type": "string",
                    "sample_values": ["87", "116", "1310", "71", "68"],
                    "description": "Number of days"
                },
                {
                    "column_name": "Category",
                    "inferred_type": "string",
                    "sample_values": [
                        "Purchases",
                        "Repairs and Maintenance Others",
                        "Site General Expenses Miscellaneous",
                        "Professional & Consultant Fees",
                        "Site Manpower Security"
                    ],
                    "description": "Expense category"
                },
                {
                    "column_name": "Risk_Level",
                    "inferred_type": "string",
                    "sample_values": ["medium", "high", "low"],
                    "description": "Level of risk"
                },
                {
                    "column_name": "Name",
                    "inferred_type": "string",
                    "sample_values": [
                        "Sandeep Vilas Sawant",
                        "Snowhill Rainbow Pvt Ltd",
                        "Harmony Group",
                        "Basavaraj J",
                        "Schoofi Software Solutions Private Limited"
                    ],
                    "description": "Name of the entity"
                }
            ],
            "random_records": [
                {
                    "Monthly_Spend": "JSA Control System",
                    "Sites": "Site Repairs and Maintenance",
                    "Outstanding": "1",
                    "Days": "425491",
                    "Category": "310752",
                    "Risk_Level": "81",
                    "Name": "high"
                },
                {
                    "Monthly_Spend": "DEC Property Management India Pvt. Ltd.",
                    "Sites": "Site Manpower Housekeeping & Soft Services",
                    "Outstanding": "4",
                    "Days": "884406",
                    "Category": "4896766",
                    "Risk_Level": "74",
                    "Name": "high"
                },
                {
                    "Monthly_Spend": "Pesto Care Services",
                    "Sites": "Site Pest Control Expenses",
                    "Outstanding": "8",
                    "Days": "78811",
                    "Category": "368784",
                    "Risk_Level": "190",
                    "Name": "high"
                },
                {
                    "Monthly_Spend": "Sahebrao Ashok Ghare",
                    "Sites": "General",
                    "Outstanding": "0",
                    "Days": "0",
                    "Category": "-20000",
                    "Risk_Level": "186",
                    "Name": "high"
                },
                {
                    "Monthly_Spend": "Santosh Gajar",
                    "Sites": "General",
                    "Outstanding": "0",
                    "Days": "0",
                    "Category": "-20000",
                    "Risk_Level": "16",
                    "Name": "low"
                }
            ]
        }

        test_cases = [
            "What is the total monthly spend?",
            "How many vendors are there for each risk level?",
            "What is the average outstanding amount by risk level?",
            "Which categories are available?",
            "Show me top 5 vendors with highest outstanding amounts",
            "What is the total outstanding for high-risk vendors?",
            "List all vendors in the Purchases category",
            "What is the average number of days by category?",
            "Which vendor has the maximum monthly spend?",
            "How many sites are managed by each risk level?",
            "What is the total outstanding amount by category?",
            "Show vendors with outstanding amount greater than 500000",
            "What is the distribution of vendors across different categories?",
            "Calculate the average monthly spend for each category",
            "Which risk level has the highest total outstanding?"
        ]

        print(f"\n{'='*80}")
        print(f"Testing SQL Answer Agent")
        print(f"Table: tbl_695ff7b55645834edb877af3")
        print(f"{'='*80}\n")

        for i, question in enumerate(test_cases, 1):
            print(f"\n{'-'*80}")
            print(f"Test Case {i}: {question}")
            print('-'*80)
            
            try:
                result = await agent.run(
                    table_name="tbl_695ff7b55645834edb877af3",
                    table_schema=test_schema,
                    user_question=question
                )
                
                print(f"\n✅ SQL Generated:")
                print(f"{result['sql']}\n")
                print(f"📝 Explanation:")
                print(f"{result['explanation']}")
                
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

        print(f"\n{'='*80}")
        print("Testing Complete")
        print(f"{'='*80}\n")

    asyncio.run(main())