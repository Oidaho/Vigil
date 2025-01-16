# ./VK-Vigil/database/__init__.py
from .db import instance
from .functiuons import connect_and_prepare, disconnect


__all__ = (
    "instance",
    "connect_and_prepare",
    "disconnect",
)
