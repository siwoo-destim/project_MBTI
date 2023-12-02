from fastapi import APIRouter, Depends, Form, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import Annotated

from BACK_TOOL.COMMON.enterance.authenticate import authenticate
from BACK.models.rooms import Room
from BACK_TOOL.COMMON.enterance.room import entrance_room_setting_private
from BACK_TOOL.COMMON.verify.name import verify_name
from BACK_SET.template.connection import templates

room_router = APIRouter()

# 라우팅]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@room_router.post("/")
async def add_room(request_user: Annotated[str, Depends(authenticate)],
                   request_room_name: Annotated[str, Form()],
                   request_room_alias: Annotated[str, Form()],
                   request_room_setting_private: Annotated[str, Depends(entrance_room_setting_private)]):
    # ――――――――――――――――――――――――――――――――――――――――――――――――――
    # 룸 이름 확인
    room_name = verify_name(request_room_name)

    if not room_name:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="name format with supplied room_name is not available."
        )

    # 중복 확인
    room = await Room.find_one(Room.room_name == request_room_name)

    if room:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room with provided room_name already exists"
        )

    # 저장
    insert_room = Room(
        room_creator=request_user,
        room_name=request_room_name,
        room_alias=request_room_alias,
        room_setting_private=request_room_setting_private
    )
    await Room.insert_one(insert_room)

    response = RedirectResponse(f"/{request_room_name}/mbti", status_code=302)
    return response

# 라우팅]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@room_router.get("/")
async def retrieve_my_rooms(request: Request,
                            request_user: Annotated[str, Depends(authenticate)]):
    # ――――――――――――――――――――――――――――――――――――――――――――――――――

    rooms = await Room.find_many(Room.room_creator == request_user).to_list()

    return templates.TemplateResponse("room.html", {
        "request": request,
        "rooms": rooms
    })
