from .models import (
    Staff,
    Peer,
    Sanction,
    Queue,
    Setting,
    ForbiddenWord,
    ForbiddenLink,
    ForbiddenHost,
)
from .db import instance


def connect_and_prepare() -> None:
    instance.connect()
    instance.create_tables(
        models=[
            Staff,
            Peer,
            Sanction,
            Queue,
            Setting,
            ForbiddenWord,
            ForbiddenLink,
            ForbiddenHost,
        ],
        safe=True,
    )


def disconnect() -> None:
    instance.close()
