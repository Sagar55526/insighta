import json
import asyncio

from app.core.config import settings
from app.core.redis import get_redis
from app.services.ws_service import manager

async def publish_event(thread_id: str, bot_message_id: str, event: dict, ):
    redis = await get_redis()

    payload = {
        "thread_id": thread_id,
        "bot_message_id": bot_message_id,
        "event": event,
    }

    await redis.publish(
        settings.REDIS_CHANNEL,
        json.dumps(payload),
    )

async def redis_event_listener():
    redis = await get_redis()

    while True:
        try:
            pubsub = redis.pubsub()
            await pubsub.subscribe(settings.REDIS_CHANNEL)
            print("🎧 Redis Listener Started")

            async for message in pubsub.listen():
                if message["type"] != "message":
                    continue

                try:
                    payload = json.loads(message["data"])

                    thread_id = payload.get("thread_id")
                    event = payload.get("event")

                    if not thread_id or not event:
                        continue

                    # sending message data to local websocket instances (backend)
                    await manager.send_message(thread_id, event)

                except Exception as e:
                    print(f"[Redis Listener] Message handling error: {e}")

        except Exception as e:
            print(f"[Redis Listener] Redis connection error: {e}")
            await asyncio.sleep(2)
