from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user
from config import configs
from db.models import Staff
import bcrypt

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
    staff = Staff.select()
    user_permision = staff.where(Staff.user_id == user_id).get().permission_lvl

    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Персонал",
        "authenticated": True,
        "authenticated_permission": user_permision,
        "staff": staff,
    }

    return templates.TemplateResponse("staff.html", context)


@router.post("/staff")
async def create_staff(
    user_id: int = Body(...),
    password: str = Body(...),
    permission_lvl: int = Body(...),
    current_id: int = Depends(get_current_user),
):
    if Staff.select().where(Staff.user_id == user_id).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким VK ID уже существует",
        )

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    Staff.create(
        user_id=user_id,
        permission_lvl=permission_lvl,
        password_hash=password_hash,
    )

    return {"message": "Сотрудник успешно добавлен"}


@router.delete("/staff/{delete_id}")
async def delete_staff(
    delete_id: int,
    user_id: int = Depends(get_current_user),
):
    if delete_id != user_id:
        staff_member = Staff.select().where(Staff.user_id == delete_id).get_or_none()
        user = Staff.select().where(Staff.user_id == user_id).get_or_none()
        if (staff_member and user) and (
            user.permission_lvl > staff_member.permission_lvl
        ):
            staff_member.delete_instance()
            return {"message": "Сотрудник удален"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить сотрудника"
    )
