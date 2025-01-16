from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user
from config import configs

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/queue", response_class=HTMLResponse)
def queue(request: Request, authenticated=Depends(get_current_user)):
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Очередь",
        "authenticated": True,
    }

    return templates.TemplateResponse("queue.html", context)
