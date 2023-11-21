from pydantic_settings import BaseSettings
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from BACK.models.mbti import MBTIPost
from BACK.models.users import User


class Settings(BaseSettings):

    DATABASE_URL: Optional[str] = None
    DATABASE_NAME: Optional[str] = None
    JWT_ACCESS_SECRET_KEY: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_database(self.DATABASE_NAME),
                          document_models=[MBTIPost, User])

    class Config:
        env_file = ".env"
