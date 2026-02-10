from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import certifi

class MongoDB:
    client: AsyncIOMotorClient = None

mongo_db = MongoDB()

async def connect_mongo():
    mongo_db.client = AsyncIOMotorClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=30000,
        # tls=True,
        # tlsCAFile=certifi.where()
    )

    # Force real connection
    await mongo_db.client.admin.command("ping")

    print("✅ MONGODB CONNECTED SUCCESSFULLY!!!")
    
async def close_mongo():
    if mongo_db.client:
        mongo_db.client.close()
        print("MONGODB CONNECTION CLOSED SUCCESSFULLY!!!")

def get_mongo_db():
    if mongo_db.client is None:
        raise RuntimeError("MongoDB not initialized!!!")
    return mongo_db.client[settings.MONGO_DB_NAME]