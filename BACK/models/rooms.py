from beanie import Document


class Room(Document):

    room_creator: str
    room_name: str
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
