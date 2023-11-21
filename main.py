from BACK.database.connection import Settings
from BACK.routes.mbti import mbti_router
from BACK.routes.users import user_router
from BACK.template.connection import templates
from BACK.authentication.authenticate import authenticate

import uvicorn

from starlette.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from typing import Annotated
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
app.include_router(mbti_router)
app.include_router(user_router, prefix="/user")

app.mount("/images", StaticFiles(directory="./FRONT/z-images/"), name="images")


# --------------------------------------------------------------------------------


@app.get("/")
async def main(request: Request, user: Annotated[str, Depends(authenticate)]):

    return templates.TemplateResponse("main.html", {
        "request": request,
        "user": user
    })


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
