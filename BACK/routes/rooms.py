from http import HTTPStatus

from fastapi import APIRouter, Depends, Form, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import Annotated

from BACK_TOOL.COMMON.enterance.authenticate import authenticate
from BACK.models.rooms import Room
from BACK.models.mbti import MBTI
from BACK_TOOL.COMMON.enterance.room import entrance_room_setting_private
from BACK_TOOL.COMMON.verify.name import verify_name
from BACK_SET.template.connection import templates
from BACK_TOOL.COMMON.verify.mbti import verify_format_name_weakly

room_router = APIRouter()


# 룸 만든는 페이지]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@room_router.get('/create')
# 룸 만드는 페이지
async def retrieve_create_room_page(request: Request,
                                    raw_user: Annotated[str, Depends(authenticate)]):
    # ――――――――――――――――――――――――――――――――――――――――――――――――――

    if not raw_user:
        response = RedirectResponse('/user/signup', status_code=302)
        return response

    return templates.TemplateResponse('room_create.html', {
        'request': request,
        'user': raw_user,
    })


# 룸 추가하기]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@room_router.post("/create")
# 룸 추가하기
async def add_room(request_user: Annotated[str, Depends(authenticate)],
                   request_room_name: Annotated[str, Form()],
                   request_room_alias: Annotated[str, Form()],
                   request_room_setting_private: Annotated[str, Depends(entrance_room_setting_private)]):
    # ――――――――――――――――――――――――――――――――――――――――――――――――――

    # 로그인 되어있는지 확인
    if not request_user:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login for creating own rooms"
        )

    # 룸 이름 확인
    verified_room_name = verify_name(request_room_name)

    if not verified_room_name:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="name format with supplied room_name is not available."
        )

    # 룸 별명 확인

    verified_room_alias = verify_format_name_weakly(request_room_alias)

    if not verified_room_alias:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="alias format with supplied room_alias is not available."
        )

    # 룸 이름에 + @
    verified_room_name = '@' + verified_room_name

    # 중복 확인
    room = await Room.find_one(Room.room_name == verified_room_name)

    if room:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room with provided room_name already exists"
        )

    # 저장
    insert_room = Room(
        room_creator=request_user,
        room_name=verified_room_name,
        room_alias=request_room_alias,
        room_setting_private=request_room_setting_private
    )
    await Room.insert_one(insert_room)

    response = RedirectResponse(f"/mbti/{verified_room_name}", status_code=302)
    return response

# 룸들 보기]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@room_router.get("/")
async def retrieve_rooms(request: Request,
                         request_user: Annotated[str, Depends(authenticate)]):
    # ――――――――――――――――――――――――――――――――――――――――――――――――――

    my_rooms = await Room.find_many(Room.room_creator == request_user).to_list()
    rooms = await Room.find_many(Room.room_creator != request_user,
                                 Room.room_setting_private == False).to_list()

    return templates.TemplateResponse("room.html", {
        "request": request,
        "user": request_user,
        "my_rooms": my_rooms,
        "rooms": rooms,
    })


@room_router.get("/delete/{room_name}")
async def delete_room(room_name: str,
                      user: Annotated[str, Depends(authenticate)]):

    room = await Room.find_one(Room.room_name == room_name)
    print(room)
    print(room_name)
    if not room:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"room with supplied roomname({room_name}) does not exists"
        )

    if not room.room_creator == user:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user} does not have permission to delete room"
        )

    await MBTI.find_many(MBTI.mbti_room == room_name).delete()
    await room.delete()

    return RedirectResponse(f'/room ', status_code=302)

