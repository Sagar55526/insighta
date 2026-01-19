# app/agents/schema_maker_agent.py
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
import re

from app.core.config import settings

PROMPT_PATH = Path(__file__).parent / "prompts" / "schema_maker_agent.md"


class SchemaMakerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            verbose=True,
        )

        self.prompt = PromptTemplate(
            template=PROMPT_PATH.read_text(),
            input_variables=["schema_payload"]
        )

        self.chain = self.prompt | self.llm | JsonOutputParser()

    async def run(self, schema_payload: dict) -> dict:
        print(f"Schema payload received: {json.dumps(schema_payload, indent=2, default=str)}")
        
        response = await self.chain.ainvoke(
            {
                "schema_payload": json.dumps(
                    schema_payload,
                    indent=2,
                    default=str
                )
            }
        )

        validated_schema = self._validate_and_fix_schema(response, schema_payload)
        
        print(f"Final schema generated: {json.dumps(validated_schema, indent=2)}")
        
        return validated_schema

    def _validate_and_fix_schema(self, response: dict, original_payload: dict) -> dict:
        if not isinstance(response, dict):
            response_str = str(response)
            response_str = re.sub(r'^```json\s*', '', response_str)
            response_str = re.sub(r'\s*```$', '', response_str)
            response = json.loads(response_str)

        schema = response.get("schema") or response.get("columns") or []
        random_records = response.get("random_records", [])

        if not random_records and "random_records" in original_payload:
            random_records = original_payload["random_records"]

        validated_schema = []
        for col in schema:
            validated_col = {
                "column_name": col.get("column_name") or col.get("name"),
                "inferred_type": col.get("inferred_type", "string"),
                "sample_values": col.get("sample_values", []),
                "description": col.get("description", "")
            }
            validated_schema.append(validated_col)

        return {
            "schema": validated_schema,
            "random_records": random_records
        }