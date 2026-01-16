from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio


from beanie import init_beanie

from app.db.mongo import connect_mongo, close_mongo, get_mongo_db
from app.models.user import User
from app.models.mapping_mng import DBMapping
from app.models.chat import Message, Thread
from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api.ingestion import router as ingest_router
from app.api.chat import router as chat_router
from app.core.config import settings
from app.services.ws_service import manager
from app.services.redis_service import redis_event_listener


@asynccontextmanager
async def lifespan(app: FastAPI):
    # App Startup
    print("🚀 App started successfully")

    await connect_mongo()

    # Initialize Beanie after Mongo is connected
    db = get_mongo_db()
    await init_beanie(
        database=db,
        document_models=[User, DBMapping, Message, Thread]
    )
    # Redis listner start listning here
    redis_task = asyncio.create_task(redis_event_listener())
    print("🚀 Redis Listener running")

    yield

    # App Shutdown
    print("🔻 Shutting down Redis listener")
    redis_task.cancel()
    try:
        await redis_task
    except asyncio.CancelledError:
        print("🛑 Redis listener cancelled")
    await close_mongo()
    print("🛑 App shutdown completed")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(ingest_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)

@app.websocket("/ws/messages/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    await manager.connect(thread_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(thread_id)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT
    )
