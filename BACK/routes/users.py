from fastapi import APIRouter, HTTPException, status, Form, Depends, Request
from BACK_TOOL.authentication.hash_password import create_hash, verify_hash
from BACK.models.users import User, TokenResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from BACK_TOOL.authentication.jwt_handler import create_access_token
from BACK_SET.template.connection import templates
from fastapi.responses import RedirectResponse
from BACK_TOOL.COMMON.verify.name import verify_name
from BACK_TOOL.COMMON.enterance.authenticate import authenticate


user_router = APIRouter()

# ---------------------------------------- 가입 ----------------------------------------


@user_router.get("/signup")
async def retrieve_sign_up_page(raw_user: Annotated[str, Depends(authenticate)],
                                request: Request):

    return templates.TemplateResponse("user_signup.html", {
        "request": request,
        "user": raw_user
    })


@user_router.post("/signup")
async def sign_user_up(username: Annotated[str, Form()],
                       password: Annotated[str, Form()]):

    # ----- USER NAME을 이용한 중복 검사

    user = await User.find_one(User.username == username)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with user_name provided already exists @@ 이 이름을 갖은 유저가 이미 존제해요!"
        )

    verified_user = verify_name(username)

    print('verified name:', verified_user)

    if not verified_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="유저 이름 이상함"
        )

    # ----- ----- PASSWORD 해쉬

    hashed_password = create_hash(password)
    tobesaved_password = hashed_password

    # ----- ----- ----- User 도큐먼트 형식으로 바꾼 후 db에 저장

    tobesaved_username = verified_user

    user = User(
        username=tobesaved_username,
        password=tobesaved_password,
    )

    await User.insert_one(user)

    access_token = create_access_token(tobesaved_username)

    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

# ---------------------------------------- 로그인 ----------------------------------------


@user_router.get("/login")
async def retrieve_sign_up_page(raw_user: Annotated[str, Depends(authenticate)],
                                request: Request):
    return templates.TemplateResponse("user_login.html", {
        "request": request,
        "user": raw_user
    })


@user_router.post("/login", response_model=TokenResponse)
async def user_login(userdata: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # USER 있는지 확인
    user = await User.find_one(User.username == userdata.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied username does not exist @@ 그런 유저이름을 갖은 계정은 없어요! -데이타베이스 올림"
        )
    # WHEN 비번 맞으면 DO 엑세스 토큰 발행
    if verify_hash(userdata.password, user.password):

        access_token = create_access_token(user.username)

        response = RedirectResponse("/", status_code=302)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response

    # 위의 상황들이 아닐때 오류
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed @@ 아마 비번이 틀릴거애요"
    )

# ---------------------------------------- 로그아웃 ----------------------------------------


@user_router.get("/logout")
async def user_logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie(key="access_token")
    return response
