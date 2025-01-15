from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user
from config import configs

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request, user_id=Depends(get_current_user)):
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Главная",
        "authenticated": True,
    }

    return templates.TemplateResponse("index.html", context)


@router.get("/conversations", response_class=HTMLResponse)
def conversations(request: Request, user_id=Depends(get_current_user)):
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Чаты",
        "authenticated": True,
    }

    return templates.TemplateResponse("conversations.html", context)


@router.get("/queue", response_class=HTMLResponse)
def queue(request: Request, user_id=Depends(get_current_user)):
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Очередь",
        "authenticated": True,
    }

    return templates.TemplateResponse("queue.html", context)


@router.get("/warns", response_class=HTMLResponse)
def warns(request: Request, user_id=Depends(get_current_user)):
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Санкции",
        "authenticated": True,
    }

    return templates.TemplateResponse("warns.html", context)


@router.get("/staff", response_class=HTMLResponse)
def staff(request: Request, user_id=Depends(get_current_user)):
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Чаты",
        "authenticated": False,
    }

    return templates.TemplateResponse("staff.html", context)
