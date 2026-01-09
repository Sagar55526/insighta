from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Any

from app.schemas.chat import (
    ThreadBase,
    ThreadResponse,
    MessageCreate,
    MessageResponse,
)
from app.models.chat import Thread
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.services.thread_service import (
    create_thread_service,
    get_thread,
    get_user_threads,
)
from app.services.message_service import (
    get_thread_messages,
    create_message,
    create_bot_message,
    update_message_content,
    update_message_graphs,
    get_table_mapping,
    get_db_id,
)
from app.utils.unified_memory_manager import UnifiedMemoryManager
from app.agents.sql_answer_agent import SQLAnswerAgent

router = APIRouter()


async def process_bot_message(
    message_in: MessageCreate,
    thread_id: str,
    user_id: str,
    bot_message_id: str,
    db_id: str,
):
    memory_manager = UnifiedMemoryManager(thread_id=thread_id)

    history_context = await memory_manager.get_history_context(
        message_in.content
    )

    # ✅ Fetch table name + schema
    mapping = await get_table_mapping(user_id=user_id, db_id=db_id)

    table_name = mapping["table_name"]
    table_schema = {
        "schema": mapping["schema"],
        "random_records": mapping["random_records"],
    }

    orchestrator_agent = SQLAnswerAgent(bot_message_id=bot_message_id)

    response = await orchestrator_agent.run(
        table_name=table_name,
        table_schema=table_schema,
        user_question=message_in.content,
        history_context=history_context,
    )

    await update_message_content(
        bot_message_id,
        response["explanation"]
    )

    if response.get("graphs"):
        await update_message_graphs(bot_message_id, response["graphs"])

    memory_manager.update_memory(
        user_query=message_in.content,
        ai_response=response["explanation"],
    )
    

@router.post(
    "/threads", response_model=ThreadResponse, status_code=status.HTTP_201_CREATED
)
async def create_thread(
    payload: ThreadBase,
    current_user=Depends(get_current_user),
):
    title = (payload.title or "").strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Title is required"
        )
    print(f"MY CURRENT USER IS IS AS FOLLOWS: {current_user}")
    return await create_thread_service(title, str(current_user.id))


@router.get("/threads", response_model=list[ThreadResponse])
async def get_threads(
    page: int = 0, limit: int = 20, current_user=Depends(get_current_user)
):
    if limit <= 0:
        limit = 20

    return await get_user_threads(user_id=str(current_user.id), page=page, limit=limit)


@router.post("/thread/{thread_id}/messages", response_model=List[MessageResponse])
async def create_new_message(
    background_tasks: BackgroundTasks,
    thread_id: str,
    message_in: MessageCreate,
    current_user=Depends(get_current_user),
) -> Any:

    # Validate thread
    thread = await get_thread(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Create user message
    user_msg = await create_message(
        content=message_in.content, user_id=str(current_user.id), thread_id=thread_id
    )

    # Create empty bot message (placeholder)
    bot_msg = await create_bot_message(
        content="", user_id=str(current_user.id), thread_id=thread_id
    )

    db_id = await get_db_id(current_user.id)

    # Background processing
    background_tasks.add_task(
        process_bot_message,
        message_in,
        thread_id,
        current_user.id,
        str(bot_msg.id),
        db_id
    )

    return [
        MessageResponse(
            id=str(user_msg.id),
            content=user_msg.content,
            is_bot=user_msg.is_bot,
            user_id=user_msg.user,
            thread_id=user_msg.thread_id,
            created_at=user_msg.created_at,
        ),
        MessageResponse(
            id=str(bot_msg.id),
            content=bot_msg.content,
            is_bot=bot_msg.is_bot,
            user_id=bot_msg.user,
            thread_id=bot_msg.thread_id,
            created_at=bot_msg.created_at,
        ),
    ]


@router.get("/threads/{thread_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    thread_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:

    thread = await Thread.get(thread_id)
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found"
        )
    print(f"MY THREAD'S OWNER IS {thread.user_id} AND CURRENT USER IS: {current_user.id}")
    if thread.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    messages = await get_thread_messages(thread_id)

    return [
        MessageResponse(
            id=str(m.id),
            content=m.content,
            is_bot=m.is_bot,
            user_id=m.user,
            thread_id=m.thread_id,
            created_at=m.created_at,
            graphs=getattr(m, "graphs", None),
            artefacts=getattr(m, "artefacts", None),
        )
        for m in messages
    ]