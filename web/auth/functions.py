from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException, Request, Response, status
from pydantic import BaseModel

from config import configs
from db.models import Staff

AUTH_COOKIE_NAME = f"{configs.PROJECT_NAME.lower()}_auth_token"


class AuthData(BaseModel):
    id: int
    permission: int
    status: bool


def authenticate_user(user_id: int, password: str) -> bool:
    user = Staff.get_or_none(Staff.id == user_id)
    if user:
        if bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            if user.permission >= 2:
                return True, None

            return False, "Lack permission"

    return False, "Invalid ID or password"


def set_current_user(response: Response, user_id: int) -> None:
    lifetime = timedelta(minutes=configs.web.jwt.TOKEN_LIFETIME)
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + lifetime,
        "iat": datetime.utcnow(),
    }

    access_token = jwt.encode(
        payload,
        key=configs.web.jwt.SECRET,
        algorithm=configs.web.jwt.ALGORITHM,
    )

    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=access_token,
        httponly=True,
        # TODO: HTTPS
        # secure=True,
        samesite="lax",
        max_age=lifetime.seconds,
    )


def get_current_user(request: Request) -> AuthData:
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
            key=configs.web.jwt.SECRET,
            algorithms=[configs.web.jwt.ALGORITHM],
        )
        user_id = int(payload["sub"])

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Invalid or expired token",
            headers={"Location": "/login"},
        )

    user = Staff.get_or_none(Staff.id == user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Invalid VK ID",
            headers={"Location": "/login"},
        )

    return AuthData(id=user.id, permission=user.permission, status=True)
