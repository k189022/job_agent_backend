from motor.motor_asyncio import AsyncIOMotorClient
from monggoDB.config.db import MONGODB_URL

async def init_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.job_agent

    # Ensure the user collection and create an index on the email field to be unique
    await db.users.create_index("email", unique=True)

    # Ensure the job collection
    await db.jobs.create_index("user_id")

    print("Database initialized and indexes created.")
