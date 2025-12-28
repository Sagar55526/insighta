from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.mongo import connect_mongo, close_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("app started successfully!!!")
    await connect_mongo()
    yield
    # Shutdown
    await close_mongo()

app = FastAPI(lifespan=lifespan)