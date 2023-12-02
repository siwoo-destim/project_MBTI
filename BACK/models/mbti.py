from beanie import Document
from typing import Optional


class MBTI(Document):
    mbti_name: str
    mbti_mbti: str
    mbti_img: Optional[str] = None
    mbti_room: Optional[str] = None

    class Settings:
        name = "mbti_post"

    class Config:
        json_schema_extra = {
            "example": {
                "mbti_name": "편라",
                "mbti_mbti": "intp",
                "mbti_img": "https://chapssalkind.com/images/nero00.jpg",
                "mbti_room": "@myroom"
            }
        }
