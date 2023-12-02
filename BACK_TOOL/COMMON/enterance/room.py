from fastapi import Form, Path
from typing import Annotated
from fastapi import HTTPException, status
from BACK_TOOL.COMMON.verify.name import verify_name


# 입구]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


async def entrance_room_setting_private(request_room_setting_private: Annotated[str, Form()]):
    if request_room_setting_private == "True":
        return True
    else:
        return False
