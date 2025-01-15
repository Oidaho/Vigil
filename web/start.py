from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import status
from fastapi import Form
from config import configs

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def is_authenticated(request: Request) -> bool:
    """Функция для проверки аутентификации на основе cookie."""
    return "auth_token" in request.cookies


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(
            "/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    context = {
        "request": request,
        "project": configs.project_name,
        "authenticated": is_authenticated(request),
    }

    return templates.TemplateResponse("index.html", context)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    context = {
        "request": request,
        "project": configs.project_name,
        "authenticated": False,
        "title": "Вход",
    }

    return templates.TemplateResponse("login.html", context)


@app.post("/login")
async def perform_login(
    response: Response, username: str = Form(...), password: str = Form(...)
):
    # Пример: проверка пользователя (добавьте вашу логику проверки)
    if username == "admin" and password == "password":  # Пример: проверка логина
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="auth_token", value="dummy_token", httponly=True)
        return response

    return RedirectResponse("/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(
        "/login",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
    response.delete_cookie("auth_token")
    return response
