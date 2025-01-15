from fastapi import APIRouter, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates
from auth import AUTH_COOKIE_NAME, get_auth, create_auth
from config import configs

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    is_authenticated, vk_id = get_auth(request=request)

    if is_authenticated:
        return RedirectResponse(
            "/",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Вход",
        "authenticated": is_authenticated,
    }

    return templates.TemplateResponse("login.html", context)


@router.post("/login")
def perform_login(vk_id: int = Form(...), password: str = Form(...)):
    response = create_auth(user_id=vk_id, password=password)
    if response is not None:
        return response

    return RedirectResponse("/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(
        "/login",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
    response.delete_cookie(AUTH_COOKIE_NAME)
    return response
