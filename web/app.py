from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import auth_router, pages_router

app = FastAPI(
    title="Web-panel",
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(pages_router)
