from beanie import Document
from typing import Optional


class MBTIPost(Document):
    name: str
    mbti: str
    img: Optional[str] = None
    room: Optional[str] = None

    class Settings:
        name = "mbti_post"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "편라",
                "mbti": "intp",
                "img": "https://chapssalkind.com/images/nero00.jpg",
                "room": "@myroom"
            }
        }
