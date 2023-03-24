from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models import UserAction


async def init_database():
    logger.debug("Established database connection")
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[UserAction]
    )
