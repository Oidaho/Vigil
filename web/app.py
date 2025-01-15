from contextlib import asynccontextmanager

import bcrypt
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import db_instance
from db.models import Staff
from config import configs
from routes import auth_router, pages_router, health_rouret


def add_admin() -> None:
    user_id = configs.web.admin_id
    hashed_password = bcrypt.hashpw(
        configs.web.password.encode("utf-8"), bcrypt.gensalt()
    )

    new_admin = Staff(
        user_id=user_id,
        permission_lvl=10,
        password_hash=hashed_password,
    )
    new_admin.save()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_instance.connect()
    add_admin()

    yield

    db_instance.close()


app = FastAPI(title="Web-panel", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(pages_router)
app.include_router(health_rouret)
