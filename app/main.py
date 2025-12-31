from fastapi import FastAPI
from contextlib import asynccontextmanager

from beanie import init_beanie

from app.db.mongo import connect_mongo, close_mongo, get_mongo_db
from app.models.user_pg import User
from app.models.mapping_mng import DBMapping
from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api.ingestion import router as ingest_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # App Startup
    print("🚀 App started successfully")

    await connect_mongo()

    # Initialize Beanie after Mongo is connected
    db = get_mongo_db()
    await init_beanie(
        database=db,
        document_models=[User, DBMapping]
    )

    yield

    # App Shutdown
    await close_mongo()
    print("🛑 App shutdown completed")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# 🔹 Include Routers
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(ingest_router, prefix=settings.API_V1_STR)