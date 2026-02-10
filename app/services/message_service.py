from datetime import datetime
from typing import List
from app.models.chat import Message
from beanie import PydanticObjectId
from app.models.mapping_mng import DBMapping



async def get_table_mapping(user_id: str, db_id: str):
    user_id = str(user_id)
    db_id = str(db_id)

    mapping = await DBMapping.find_one(
        DBMapping.user_id == user_id,
        DBMapping.db_id == db_id,
    )

    if not mapping:
        raise ValueError(
            f"No completed schema found for user_id={user_id}, db_id={db_id}"
        )

    return {
        "table_name": mapping.table_name,
        "schema": mapping.schema,
        "random_records": mapping.random_records,
    }


async def get_all_table_mappings(user_id: str):
    user_id = str(user_id)

    mappings = await DBMapping.find(
        DBMapping.user_id == user_id,
    ).to_list()

    if not mappings:
        raise ValueError(
            f"No completed schemas found for user_id={user_id}"
        )

    return [
        {
            "table_name": mapping.table_name,
            "schema": mapping.schema,
            "random_records": mapping.random_records,
        }
        for mapping in mappings
    ]



async def create_message(content: str, user_id: str, thread_id: str) -> Message:
    """
    Create and save a bot message.
    """
    message = Message(
        content=content,
        user=user_id,
        thread_id=thread_id,
        is_bot=False,
        created_at=datetime.utcnow(),
    )
    await message.insert()
    return message


async def create_bot_message(content: str, user_id: str, thread_id: str) -> Message:
    """
    Create and save a bot message.
    """
    message = Message(
        content=content,
        user=user_id,
        thread_id=thread_id,
        is_bot=True,
        created_at=datetime.utcnow(),
    )
    await message.insert()
    return message


async def get_thread_messages(thread_id: str):
    return await (
        Message.find(Message.thread_id == thread_id).sort("+created_at").to_list()
    )


async def update_message_content(message_id: str, content: str):
    await Message.find(Message.id == PydanticObjectId(message_id)).update(
        {"$set": {"content": content}}
    )


async def update_message_graphs(message_id: str, graphs: list):
    await Message.find(Message.id == PydanticObjectId(message_id)).update(
        {"$set": {"graphs": graphs}}
    )


async def update_message_artefacts(message_id: str, artefacts: list):
    await Message.find(Message.id == PydanticObjectId(message_id)).update(
        {"$set": {"artefacts": artefacts}}
    )

async def get_db_id(user_id: str) -> str:
    user_id = str(user_id)
    print(f"USER ID GOT IS AS FOLLOWS: {user_id}")

    mapping = await DBMapping.find_one(
        DBMapping.user_id == user_id
    )
    if not mapping:
        raise ValueError("No DB mapping found in records!!!")
    return mapping.db_id
