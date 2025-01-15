from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from auth import get_auth
from config import configs

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    is_authenticated, vk_id = get_auth(request=request)

    if not is_authenticated:
        return RedirectResponse(
            "/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Главная",
        "authenticated": is_authenticated,
    }

    return templates.TemplateResponse("index.html", context)


@router.get("/conversations", response_class=HTMLResponse)
def conversations(request: Request):
    is_authenticated, vk_id = get_auth(request=request)

    if not is_authenticated:
        return RedirectResponse(
            "/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Чаты",
        "authenticated": is_authenticated,
    }

    return templates.TemplateResponse("conversations.html", context)


@router.get("/queue", response_class=HTMLResponse)
def queue(request: Request):
    is_authenticated, vk_id = get_auth(request=request)

    if not is_authenticated:
        return RedirectResponse(
            "/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Очередь",
        "authenticated": is_authenticated,
    }

    return templates.TemplateResponse("queue.html", context)


@router.get("/warns", response_class=HTMLResponse)
def warns(request: Request):
    is_authenticated, vk_id = get_auth(request=request)

    if not is_authenticated:
        return RedirectResponse(
            "/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Санкции",
        "authenticated": is_authenticated,
    }

    return templates.TemplateResponse("warns.html", context)


@router.get("/staff", response_class=HTMLResponse)
def staff(request: Request):
    is_authenticated, vk_id = get_auth(request=request)

    if not is_authenticated:
        return RedirectResponse(
            "/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Чаты",
        "authenticated": is_authenticated,
    }

    return templates.TemplateResponse("staff.html", context)
