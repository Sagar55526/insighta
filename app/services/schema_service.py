from app.db.postgres_introspection import get_table_context
from app.agents.schema_maker_agent import schema_graph
from app.models.mapping_mng import DBMapping
from sqlalchemy.ext.asyncio import AsyncSession


async def generate_schema(
    mapping_id: str,
    pg_session: AsyncSession
):
    mapping = await DBMapping.get(mapping_id)

    context = await get_table_context(
        pg_session,
        mapping.table_name
    )

    result = schema_graph.invoke({
        "columns": context["columns"],
        "samples": context["samples"]
    })

    mapping.schema = result["schema"]
    await mapping.save()

    return mapping
