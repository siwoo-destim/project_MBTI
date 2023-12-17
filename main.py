from BACK_SET.database.connection import Settings
from BACK.routes.mbti import mbti_router
from BACK.routes.users import user_router
from BACK.routes.rooms import room_router
from BACK_SET.template.connection import templates
from BACK_TOOL.COMMON.enterance.authenticate import authenticate

import uvicorn

from starlette.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from typing import Annotated
from fastapi.responses import RedirectResponse
# --------------------------------------------------------------------------------

# 데이터베이스 세팅
settings = Settings()


# 시작할때 데이터베이스를 initalize한다
@asynccontextmanager
async def lifespan(app: FastAPI):
    # WHEN 시작할때 DO 데이터베이스 키기
    await settings.initialize_database()
    yield
    # WHEN 꺼질떄 DO NOTHING
    pass

# APP 연결
app = FastAPI(lifespan=lifespan)

# 고정 경로 설정

app.include_router(user_router, prefix="/user")
app.include_router(room_router, prefix="/room")
app.include_router(mbti_router, prefix="/mbti")

app.mount("/images", StaticFiles(directory="./store/"), name="images")
app.mount('/css', StaticFiles(directory='./FRONT/css/'), name='css')
app.mount('/js', StaticFiles(directory='./FRONT/js/'), name='js')


# --------------------------------------------------------------------------------


@app.get("/explain")
async def retrieve_explain_page(request: Request, user: Annotated[str, Depends(authenticate)]):

    return templates.TemplateResponse("explain.html", {
        "request": request,
        "user": user
    })


@app.get('/')
async def redirect_page(user: Annotated[str, Depends(authenticate)]):

    if user:
        return RedirectResponse('/room', status_code=302)
    else:
        return RedirectResponse('/explain', status_code=302)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
