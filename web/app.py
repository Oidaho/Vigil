from contextlib import asynccontextmanager

import bcrypt
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import db_isntanse
from routes import auth_router, pages_router


def add_admin() -> None:
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_isntanse.connect()

    yield

    db_isntanse.close()


app = FastAPI(title="Web-panel", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(pages_router)
