from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user
from config import configs
from db.models import Conversation, Setting, Delay

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/conversations", response_class=HTMLResponse)
def conversations(request: Request, authenticated=Depends(get_current_user)):
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
    authenticated=Depends(get_current_user),
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
def delete_conversation(peer_id: int, authenticated=Depends(get_current_user)):
    conversation = (
        Conversation.select().where(Conversation.peer_id == peer_id).get_or_none()
    )
    if conversation:
        conversation.delete_instance()
        return {"message": "Метка беседы снята"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось снять метку беседы"
    )
