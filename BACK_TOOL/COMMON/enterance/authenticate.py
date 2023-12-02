from fastapi import Request
from BACK_TOOL.authentication.jwt_handler import verify_access_token


async def authenticate(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        return False

    decoded_token = verify_access_token(token)

    result = decoded_token.get("user")
    return result
