import pymongo
from beanie import Document, Indexed
from pydantic import BaseModel


class RoomFilterOnAlias(BaseModel):
    room_alias: str


class Room(Document):

    room_creator: str
    room_name: Indexed(str, index_type=pymongo.TEXT)
    room_alias: str

    room_setting_private: bool

    class Settings:
        name = "rooms"

    class Config:
        json_schema_extra = {
            "example": {
                "room_creator": "chapssal_kind",
                "room_name": "myroom",
                "room_alias": "chapssal's room"
            }
        }
