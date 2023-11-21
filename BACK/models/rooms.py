from beanie import Document
from typing import Optional


class Room(Document):
    creator: str
    roomname: str
    alias: Optional[str] = None

    class Settings:
        name = "rooms"

    class Config:
        json_schema_extra = {
            "example": {
                "creator": "chapssal_kind",
                "roomname": "myroom",
                "alias": "chapssal's room"
            }
        }
