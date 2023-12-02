from BACK_SET.database.connection import Settings
from NERO import nero_time
from jose import jwt, JWTError
import time
from fastapi import HTTPException, status


settings = Settings()

# 토큰 시크릿 키
jwt_access_secret_key = settings.JWT_ACCESS_SECRET_KEY
# 토큰 지속 시간 ( nero_time serves the function of converting units like days into seconds(int) )
access_token_lifetime = nero_time.nero_time(days=30)

# -------------------- 토큰 만들기 --------------------


def payload_template(user: str, lifetime: int) -> dict:
    expires = time.time() + lifetime

    payload = {
        "user": user,
        "expires": expires
    }

    return payload


def create_access_token(user: str) -> str:
    payload = payload_template(user=user,
                               lifetime=access_token_lifetime)

    token = jwt.encode(payload, jwt_access_secret_key, algorithm="HS256")

    return token


def verify_access_token(token: str):
    try:
        data = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=["HS256"])
        expires = data.get("expires")

        if expires is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )

        if expires < time.time():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired"
            )
        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
