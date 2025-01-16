from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user
from config import configs
from db.models import Staff, Conversation, Setting, Delay
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


# ! Conversations
@router.get("/conversations", response_class=HTMLResponse)
def conversations(request: Request, user_id=Depends(get_current_user)):
    peers = Conversation.select()
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Чаты",
        "authenticated": True,
        "conversations": peers,
    }

    return templates.TemplateResponse("conversations.html", context)


@router.patch("/conversations/{peer_id}")
def update_conversation(
    peer_id: int,
    settings: list = Body(...),
    delays: list = Body(...),
    user_id=Depends(get_current_user),
):
    conversation = Conversation.get_or_none(Conversation.peer_id == peer_id)
    if conversation:
        for setting_update in settings:
            if "id" not in setting_update or "is_enabled" not in setting_update:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Неверный формат данных для настройки. Ожидаются 'id' и 'is_enabled'.",
                )

            setting = Setting.get_or_none(
                Setting.id == setting_update["id"],
                Setting.conversation == conversation,
            )
            if setting:
                setting.is_enabled = bool(int(setting_update["is_enabled"]))
                setting.save()

        for delay_update in delays:
            if "id" not in delay_update or "count" not in delay_update:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Неверный формат данных для задержки. Ожидаются 'id' и 'count'.",
                )

            delay = Delay.get_or_none(
                Delay.id == delay_update["id"],
                Delay.conversation == conversation,
            )
            if delay:
                delay.count = delay_update["count"]
                delay.save()

        return {"message": "Настройки успешно обновлены"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Неверный формат данных. Ожидаются списки 'settings' и 'delays'.",
    )


@router.delete("/conversations/{peer_id}")
def delete_conversation(peer_id: int, user_id=Depends(get_current_user)):
    conversation = (
        Conversation.select().where(Conversation.peer_id == peer_id).get_or_none()
    )
    if conversation:
        conversation.delete_instance()
        return {"message": "Метка беседы снята"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось снять метку беседы"
    )


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


# ! Staff
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
def create_staff(
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
def delete_staff(
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
