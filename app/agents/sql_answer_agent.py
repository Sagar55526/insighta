from pathlib import Path
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


PROMPT_PATH = Path(__file__).parent / "prompts" / "sql_answer_agent.md"


class SQLAnswerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )

        self.prompt = PromptTemplate(
            template=PROMPT_PATH.read_text(),
            input_variables=["query_payload"],
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    async def run(
        self,
        table_name: str,
        table_schema: dict,
        user_question: str,
    ) -> dict:
        payload = {
            "table_name": table_name,
            "table_schema": table_schema,
            "user_question": user_question,
        }

        response = await self.chain.ainvoke(
            {"query_payload": json.dumps(payload, indent=2)}
        )
        cleaned = response.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```json").removeprefix("```")
            cleaned = cleaned.removesuffix("```").strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"SQLAnswerAgent returned invalid JSON:\n{cleaned}"
            ) from e


import asyncio

if __name__ == "__main__":
    async def main():
        agent = SQLAnswerAgent()

        result = await agent.run(
            table_name="695ea50f5614a6605cc1cc62_tbl",
            table_schema={
            "schema": [
            {
                "column_name": "Name",
                "inferred_type": "string",
                "sample_values": [
                "Bajaj Finance Limited–Weikfield",
                "PHN Technology Pvt Ltd-PUFM/00110",
                "Dhishan Bulwark Private Limited-KAFM/00069",
                "Vodafone Digilink Limited (Hry)",
                "Volvo India Pvt Ltd. Gurgaon"
                ],
                "description": "The name of the vendors(service providers)."
            },
            {
                "column_name": "Region",
                "inferred_type": "string",
                "sample_values": [
                "South - Karnataka - Bangalore",
                "South - Karnataka - Bangalore",
                "West - Maharashtra - Pune",
                "South - Tamilnadu - Chennai",
                "South - Hyderabad"
                ],
                "description": "The geographical region of the company."
            },
            {
                "column_name": "Type",
                "inferred_type": "string",
                "sample_values": [
                "Facilities & Asset Management Services",
                "Facilities & Asset Management Services",
                "Facilities & Asset Management Services",
                "Facilities & Asset Management Services",
                "Facilities & Asset Management Services"
                ],
                "description": "The type of services provided by the company."
            },
            {
                "column_name": "Monthly Spend",
                "inferred_type": "string",
                "sample_values": [
                0,
                440030,
                0,
                709617,
                0
                ],
                "description": "The monthly expenditure of the company."
            },
            {
                "column_name": "Vendors",
                "inferred_type": "integer",
                "sample_values": [
                4,
                2,
                1,
                4,
                0
                ],
                "description": "The number of vendors associated with the company."
            },
            {
                "column_name": "Outstanding",
                "inferred_type": "integer",
                "sample_values": [
                20000,
                1071419,
                29962,
                0,
                5891959
                ],
                "description": "The outstanding amount owed by the company."
            },
            {
                "column_name": "Days",
                "inferred_type": "integer",
                "sample_values": [
                0,
                2326,
                0,
                0,
                509
                ],
                "description": "The number of days related to financial metrics."
            },
            {
                "column_name": "DSO",
                "inferred_type": "integer",
                "sample_values": [
                99,
                0,
                154,
                0,
                214
                ],
                "description": "Days Sales Outstanding, a measure of how quickly receivables are collected."
            },
            {
                "column_name": "DPO",
                "inferred_type": "integer",
                "sample_values": [
                72,
                63,
                65,
                152,
                0
                ],
                "description": "Days Payable Outstanding, a measure of how quickly payables are settled."
            },
            {
                "column_name": "Risk Level",
                "inferred_type": "category",
                "sample_values": [
                "low",
                "low",
                "medium",
                "high",
                "high"
                ],
                "description": "The risk level associated with the company."
            }
            ],
            "random_records": [
            {
                "Name": "Bajaj Auto Limited -Vijayawada",
                "Region": "South - Hyderabad",
                "Type": "Facilities & Asset Management Services",
                "Monthly Spend": "0",
                "Vendors": "2",
                "Outstanding": "118934",
                "Days": "102",
                "DSO": "102",
                "DPO": "82",
                "Risk Level": "high"
            },
            {
                "Name": "Rusel Multiventures Private Limited-MUFM/00087",
                "Region": "West - Maharashtra - Mumbai",
                "Type": "Facilities & Asset Management Services",
                "Monthly Spend": "1008460",
                "Vendors": "7",
                "Outstanding": "330256",
                "Days": "391",
                "DSO": "391",
                "DPO": "72",
                "Risk Level": "high"
            }
            ]
            },
            user_question="what is risk level wise total count of vendors ?",
        )

        print(result)

    asyncio.run(main())
