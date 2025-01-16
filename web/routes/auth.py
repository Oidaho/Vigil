from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates
from auth import AUTH_COOKIE_NAME, set_current_user, authenticate_user
from config import configs

templates = Jinja2Templates(directory="templates")
router = APIRouter()


def render_login_page(request: Request, error: str | None) -> HTMLResponse:
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Вход",
        "authenticated": False,
        "error": error,
    }

    return templates.TemplateResponse("login.html", context)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return render_login_page(request=request, error=None)


@router.post("/login")
def login(request: Request, user_id: int = Form(...), password: str = Form(...)):
    is_authenticated, error = authenticate_user(user_id, password)

    if not is_authenticated:
        return render_login_page(request=request, error=error)

    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    set_current_user(response, user_id)

    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(
        "/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
    response.delete_cookie(AUTH_COOKIE_NAME)
    return response
