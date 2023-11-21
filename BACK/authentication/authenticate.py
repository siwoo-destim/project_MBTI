from fastapi import Depends, HTTPException, status, Request
from BACK.authentication.jwt_handler import verify_access_token


async def authenticate(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        return False

    decoded_token = verify_access_token(token)

    result = decoded_token.get("user")
    return result
