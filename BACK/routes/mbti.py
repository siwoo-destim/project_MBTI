from BACK.models.mbti import MBTIPost
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from typing import Annotated
from BACK.template.connection import templates
from BACK.rooms.verify_room import verify_room

mbti_router = APIRouter()


@mbti_router.get("/{roomname}/mbti")
async def retrieve_mbti_posts(request: Request,
                              roomname: str):

    room = verify_room(roomname)

    mbti_posts = await MBTIPost.find_many(MBTIPost.room == room).to_list()

    templates.TemplateResponse("[roomname]mbti.html", {
        "request": request,
        "mbti_posts": mbti_posts
    })


@mbti_router.post("/{roomname}/mbti")
async def add_mbti_post(name: Annotated[str, Form()],
                        mbti: Annotated[str, Form()],
                        roomname: str):

    room = verify_room(roomname)

    mbti_post = MBTIPost(
        name=name,
        mbti=mbti,
        img="127.0.0.1/images/lalo_salamanca.webp",
        room=room.roomname
    )

    await MBTIPost.insert_one(mbti_post)

    return RedirectResponse(f"/{room}", status_code=302)
