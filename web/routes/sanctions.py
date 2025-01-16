from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user
from config import configs
from db.models import Conversation, Sanction

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/sanctions", response_class=HTMLResponse)
def sanctions_page(
    request: Request,
    authenticated=Depends(get_current_user),
):
    peers = Conversation.select()
    context = {
        "request": request,
        "project": configs.project_name,
        "title": "Санкции",
        "authenticated": True,
        "conversations": peers,
        "max_warns": configs.bot.max_warns,
    }

    return templates.TemplateResponse("sanctions.html", context)


@router.patch("/sanctions")
def update_sanction(
    peer_id: int = Body(...),
    user_id: int = Body(...),
    authenticated=Depends(get_current_user),
):
    peer = Conversation.get_or_none(Conversation.peer_id == peer_id)
    if peer:
        sanction = Sanction.get_or_none(
            Sanction.conversation == peer,
            Sanction.user_id == user_id,
        )
        if sanction:
            sanction.warns_count -= 1
            if sanction.warns_count <= 0:
                sanction.delete_instance()
            else:
                sanction.save()

            return {"message": "Очки санкции учпешно декрементированны"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Не удалось декрементировать очки санкциий.",
    )


@router.delete("/sanctions")
def delete_sanction(
    peer_id: int = Body(...),
    user_id: int = Body(...),
    authenticated=Depends(get_current_user),
):
    peer = Conversation.get_or_none(Conversation.peer_id == peer_id)
    if peer:
        sanction = Sanction.get_or_none(
            Sanction.conversation == peer,
            Sanction.user_id == user_id,
        )
        if sanction:
            sanction.delete_instance()
            return {"message": "Санкция удалена"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Не удалось удалить санкцию.",
    )
