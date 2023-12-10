from BACK.models.mbti import MBTI
from fastapi import APIRouter, Form, Request, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import Annotated
from BACK_SET.template.connection import templates
from BACK.models.rooms import Room
from BACK_TOOL.COMMON.enterance.mbti import entrance_of_mbti_mbti_asform, entrance_of_mbti_name_asform
from BACK_TOOL.COMMON.verify.mbti import verify_format_name_weakly, verify_format_mbti_mbti
from BACK_SET.database.connection import Settings
from BACK_TOOL.COMMON.enterance.authenticate import authenticate
import uuid
import os

mbti_router = APIRouter()

settings = Settings()

image_store_url = settings.IMAGE_STORE_DIR

# IN 룸 DO mbti 포스트 보기]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mbti_router.get("/{path_request_room_name}/mbti")
async def retrieve_mbti_posts(raw_user: Annotated[str, Depends(authenticate)],
                              path_request_room_name: str,
                              request: Request):
    # ――――――――――――――――――――――――――――――――――――――――――――――――――

    # 룸 있나 검증

    room = await Room.find_one(Room.room_name == path_request_room_name)

    if not room:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="room with supplied room_name does not exist"
        )

    # ――――――――――――――――――――――――――――――――――――――――――――――――――
    # mbti 포스트 찾기
    mbti_posts = await MBTI.find_many(MBTI.mbti_room == path_request_room_name).to_list()

    if not mbti_posts:
        mbti_posts = []

    return templates.TemplateResponse("[roomname]mbti.html", {
        "request": request,
        "user": raw_user,
        "mbti_posts": mbti_posts,
        "room": room
    })


# IN 룸 DO 룸 만들기]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mbti_router.get("/{path_request_room_name}/mbti/create")
async def retrieve_mbti_create_page(raw_user: Annotated[str, Depends(authenticate)],
                                    request: Request):
    return templates.TemplateResponse("[roomname]mbti_create.html", {
        "request": request,
        "user": raw_user
    })


@mbti_router.post("/{path_request_room_name}/mbti/create")
async def add_mbti_post(path_request_room_name: str,
                        request_mbti_name: Annotated[str, Form()],
                        request_mbti_mbti: Annotated[str, Form()],
                        raw_mbti_image: UploadFile):
    # ――――――――――――――――――――――――――――――――――――――――――――――――――

    mbti_name = verify_format_name_weakly(request_mbti_name)

    if not mbti_name:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='mbti_name with supplied name does not follow own format'
        )

    mbti_mbti = verify_format_mbti_mbti(request_mbti_mbti)

    if not mbti_mbti:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='mbti_mbti with supplied mbti does not follow own format'
        )

    # ――――――――――――――――――――――――――――――――――――――――――――――――――

    # 룸 존제 여부
    room = await Room.find_one(Room.room_name == path_request_room_name)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room with supplied rome_name does not exist"
        )
    content = await raw_mbti_image.read()
    photo_filename = f"{str(uuid.uuid4())}.jpg"
    with open(os.path.join(image_store_url, photo_filename), "wb") as fp:
        fp.write(content)


    # 포스트
    mbti_post = MBTI(
        mbti_name=mbti_name,
        mbti_mbti=mbti_mbti,
        mbti_img=photo_filename,
        mbti_room=path_request_room_name
    )

    await MBTI.insert_one(mbti_post)

    return RedirectResponse(f"/{path_request_room_name}/mbti", status_code=302)
