from typing import Tuple

from fastapi import Request, Response, status
from fastapi.responses import RedirectResponse

from config import configs
from datetime import datetime, timezone, timedelta

from .jwt import decode_token, encode_token

AUTH_COOKIE_NAME = f"{configs.project_name}_auth_token"


def get_auth(request: Request) -> Tuple[bool, int | None]:
    token = request.cookies.get(AUTH_COOKIE_NAME)
    if token is None:
        return False, None

    payload = decode_token(token)
    if payload is None:
        return False, None

    user_id = int(payload.get("sub"))
    if user_id is None:
        return False, None

    return True, user_id


def create_auth(user_id: int, password: str) -> Response | None:
    if user_id == 1 and password == "password":
        now = datetime.now(tz=timezone.utc)
        exp = now + timedelta(minutes=configs.web.jwt.access_token_lifetime)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": exp,
        }
        access_token = encode_token(payload)

        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key=AUTH_COOKIE_NAME, value=access_token, httponly=True)
        return response

    return None
