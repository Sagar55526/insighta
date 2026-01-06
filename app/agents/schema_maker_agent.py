from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

from app.core.config import settings


PROMPT_PATH = Path(__file__).parent / "prompts" / "schema_maker_agent.md"


class SchemaMakerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        self.prompt = PromptTemplate(
            template=PROMPT_PATH.read_text(),
            input_variables=["schema_payload"]
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    async def run(self, schema_payload: dict) -> dict:
        """
        Runs schema inference agent and returns parsed JSON
        """
        print(f"schema payload is as follows: {schema_payload}")
        response = await self.chain.ainvoke(
            {
                "schema_payload": json.dumps(
                    schema_payload,
                    indent=2,
                    default=str
                )
            }
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError("SchemaMakerAgent returned invalid JSON")
