# app/services/schema_maker_service.py
from datetime import datetime
from app.agents.schema_maker_agent import SchemaMakerAgent
from app.models.mapping_mng import DBMapping


async def generate_and_store_schema(
    mapping: DBMapping,
    schema_payload: dict
):
    agent = SchemaMakerAgent()

    inferred_schema = await agent.run(schema_payload)

    mapping.schema = inferred_schema.get("schema", [])
    mapping.random_records = inferred_schema.get("random_records", [])
    mapping.schema_status = "COMPLETED"
    mapping.schema_created_at = datetime.utcnow()

    await mapping.save()

    return inferred_schema