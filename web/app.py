from contextlib import asynccontextmanager

import bcrypt
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import db_instance
from db.models import Staff
from config import configs
from routes import (
    auth_,
    health_,
    index_,
    peers_,
    queue_,
    sanctions_,
    staff_,
)


def add_admin() -> None:
    user_id = configs.web.admin_id
    hashed_password = bcrypt.hashpw(
        configs.web.password.encode("utf-8"), bcrypt.gensalt()
    )

    new_admin, created = Staff.get_or_create(
        user_id=user_id,
        defaults={
            "permission_lvl": 10,
            "password_hash": hashed_password,
        },
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_instance.connect()
    add_admin()

    yield

    db_instance.close()


app = FastAPI(title="Web-panel", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_)
app.include_router(health_)
app.include_router(index_)
app.include_router(peers_)
app.include_router(queue_)
app.include_router(sanctions_)
app.include_router(staff_)
