from beanie import Document
from pydantic import BaseModel
from typing import List, Optional


class User(Document):
    username: str
    password: str
    rooms_user_has: Optional[List[str]] = []

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "chapssal_kind",
                "password": "strong!!!"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

