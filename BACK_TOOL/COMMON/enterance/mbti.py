from BACK_TOOL.COMMON.verify.mbti import verify_format_name_weakly, verify_format_mbti_mbti
from fastapi import Form, HTTPException, status
from typing import Annotated


async def entrance_of_mbti_name_asform(request_mbti_name: Annotated[str, Form()]):
    mbti_name = verify_format_name_weakly(request_mbti_name)

    if not mbti_name:

        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='mbti_name with supplied name does not follow own format'
        )


async def entrance_of_mbti_mbti_asform(request_mbti_mbti: Annotated[str, Form()]):
    mbti_mbti = verify_format_mbti_mbti(request_mbti_mbti)

    if not mbti_mbti:

        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='mbti_mbti with supplied mbti does not follow own format'
        )
