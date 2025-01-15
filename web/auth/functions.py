from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Request, Response, status

from config import configs

AUTH_COOKIE_NAME = f"{configs.project_name}_auth_token"


def authenticate_user(user_id: int, password: str) -> bool:
    # TODO: Хеширование пароля и работа с БД
    return user_id == 1 and password == "password"


def set_current_user(response: Response, user_id: int) -> None:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow()
        + timedelta(minutes=configs.web.jwt.access_token_lifetime),
        "iat": datetime.utcnow(),
    }

    access_token = jwt.encode(
        payload,
        key=configs.web.jwt.secret,
        algorithm=configs.web.jwt.algorithm,
    )

    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=access_token,
        httponly=True,
        # TODO: HTTPS
        # secure=True,
        samesite="lax",
        max_age=3600,
    )


def get_current_user(request: Request) -> int:
    token = request.cookies.get(AUTH_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Not authenticated",
            headers={"Location": "/login"},
        )

    try:
        payload = jwt.decode(
            jwt=token,
            key=configs.web.jwt.secret,
            algorithms=[configs.web.jwt.algorithm],
        )
        user_id = int(payload["sub"])

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Invalid or expired token",
            headers={"Location": "/login"},
        )

    # TODO: Подойдет для получения данных со страницы VK
    # user_info = get_user_info(vk_id)

    return user_id
