from typing import Dict, NoReturn, Tuple

import jwt
from fastapi import Request

from config import configs


Payload = Dict[str, int | str]


def decode_token(token: str) -> Payload | None:
    try:
        payload = jwt.decode(
            jwt=token,
            key=configs.web.jwt.secret,
            algorithms=[configs.web.jwt.algorithm],
        )

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

    return payload


def encode_token(payload: Payload) -> str | None:
    try:
        token = jwt.encode(
            payload=payload,
            key=configs.web.jwt.secret,
            algorithm=configs.web.jwt.algorithm,
        )

    except Exception:
        return None

    return token
