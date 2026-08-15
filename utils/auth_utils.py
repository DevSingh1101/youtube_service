from fastapi import Request, HTTPException
from http import HTTPStatus
from typing import List

from core import TokenManager

def get_encoded_payload(token_manager: TokenManager, request: Request, cookie_key: str, required_fields: List[str] = None) -> dict:
    access_token: str | None = request.cookies.get(cookie_key)

    if not access_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Login again to get access, as token has expired",
        )

    try:
        payload = token_manager.decode_access_token(access_token)

        if not payload or not all(payload.get(field) for field in required_fields):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid or expired access token, please login again to get a new access token",
            )

        return payload
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid or expired access token, please login again to get a new access token",
        )