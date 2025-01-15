from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import auth_router, pages_router
from contextlib import asynccontextmanager
from db import get_db_isntanse


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db_isntanse()
    db.connect()

    yield

    db.close()


app = FastAPI(title="Web-panel", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(pages_router)
