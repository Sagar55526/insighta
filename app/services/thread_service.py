from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from app.models.chat import Thread as ThreadDocument
from app.schemas.chat import ThreadResponse


async def create_thread_service(title: str, user_id: str) -> ThreadResponse:
    try:
        now = datetime.utcnow()
        thread_doc = ThreadDocument(
            title=title,
            user_id=user_id,
            created_at=now,
            updated_at=now,
        )
        await thread_doc.insert()

        return ThreadResponse(
            id=str(thread_doc.id),
            title=thread_doc.title,
            user_id=thread_doc.user_id,
            created_at=thread_doc.created_at,
            updated_at=thread_doc.updated_at,
        )

    except Exception as e:
        raise ValueError("Failed to create thread") from e


async def get_user_threads(user_id: str, page: int, limit: int) -> List[ThreadResponse]:
    try:
        skip = page * limit

        threads = (
            await ThreadDocument.find(ThreadDocument.user_id == user_id)
            .sort("-created_at")
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        return [
            ThreadResponse(
                id=str(t.id),
                title=t.title,
                user_id=t.user_id,
                created_at=t.created_at,
                updated_at=t.updated_at,
            )
            for t in threads
        ]

    except Exception as e:
        raise ValueError(f"Failed to retrieve user threads: {e}")


async def get_thread(thread_id: str) -> Optional[ThreadResponse]:
    try:
        # Just for security added validation here.
        if not PydanticObjectId.is_valid(thread_id):
            raise ValueError("Invalid thread ID format")

        thread = await ThreadDocument.get(thread_id)
        if not thread:
            return None

        return ThreadResponse(
            id=str(thread.id),
            title=thread.title,
            user_id=thread.user_id,
            created_at=thread.created_at,
            updated_at=thread.updated_at,
        )

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to fetch thread: {e}")


async def get_user_default_thread(user_id: str) -> Optional[ThreadResponse]:
    try:
        thread = await ThreadDocument.find_one(
            ThreadDocument.user_id == user_id,
            ThreadDocument.title == "default"
        )

        if not thread:
            return None

        return ThreadResponse(
            id=str(thread.id),
            title=thread.title,
            user_id=thread.user_id,
            created_at=thread.created_at,
            updated_at=thread.updated_at,
        )

    except Exception as e:
        raise ValueError(f"Failed to fetch user's default thread: {e}")
