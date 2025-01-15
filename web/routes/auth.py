from fastapi import APIRouter, Form, Request, Response, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates
from auth import AUTH_COOKIE_NAME, set_current_user, authenticate_user
from config import configs

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Вход",
        "authenticated": False,
    }

    return templates.TemplateResponse("login.html", context)


@router.post("/login")
def login(response: Response, user_id: int = Form(...), password: str = Form(...)):
    is_authenticated = authenticate_user(user_id, password)

    if not is_authenticated:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    set_current_user(response, user_id)

    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(
        "/login",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
    response.delete_cookie(AUTH_COOKIE_NAME)
    return response
