from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict, List


class SchemaState(TypedDict):
    columns: List[dict]
    samples: List[dict]
    schema: List[dict]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def schema_maker_node(state: SchemaState) -> SchemaState:
    prompt = f"""
You are a data architect.

Given:
Columns:
{state['columns']}

Sample rows:
{state['samples']}

Return JSON schema:
[
  {{
    "column_name": "",
    "dtype": "",
    "description": "",
    "sample_values": []
  }}
]
"""

    response = llm.invoke(prompt)
    state["schema"] = response.json()
    return state


graph = StateGraph(SchemaState)
graph.add_node("schema_maker", schema_maker_node)
graph.set_entry_point("schema_maker")

schema_graph = graph.compile()
