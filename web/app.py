from contextlib import asynccontextmanager

import bcrypt
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import connect_and_prepare, disconnect
from db.models import Staff
from config import configs
from routes import (
    auth_router,
    health_router,
    index_router,
    peers_router,
    staff_router,
)


def add_admin() -> None:
    user_id = configs.web.admin_id
    hashed_password = bcrypt.hashpw(
        configs.web.password.encode("utf-8"), bcrypt.gensalt()
    )

    new_admin, created = Staff.get_or_create(
        id=user_id,
        defaults={
            "permission": 3,
            "password_hash": hashed_password,
        },
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # db
    connect_and_prepare()
    add_admin()

    yield

    # db
    disconnect()


app = FastAPI(title="Web-panel", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(index_router)
app.include_router(peers_router)
app.include_router(staff_router)
