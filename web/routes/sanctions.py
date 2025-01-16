from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user
from config import configs
from db.models import Staff, Conversation, Setting, Delay, Sanction
import bcrypt

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/sanctions", response_class=HTMLResponse)
def sanctions(
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
    request: Request,
    peer_id: int = Body(...),
    user_id: int = Body(...),
    authenticated=Depends(get_current_user),
):
    pass


@router.patch("/sanctions")
def delete_sanction(
    request: Request,
    peer_id: int = Body(...),
    user_id: int = Body(...),
    authenticated=Depends(get_current_user),
):
    peer = ...
