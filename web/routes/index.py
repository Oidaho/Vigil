from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user
from config import configs

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request, authenticated=Depends(get_current_user)):
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Главная",
        "authenticated": True,
    }

    return templates.TemplateResponse("index.html", context)
