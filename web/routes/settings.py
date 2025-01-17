from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from auth import AuthData, get_current_user
from config import configs
from db.models import ForbiddenHost, ForbiddenLink, ForbiddenWord, Peer, Setting

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/{peer_id}/settings")


# class SettingsData(BaseModel):
#     settings: Optional[...]
#     forbidden_links: Optional[...]
#     forbidden_hosts: Optional[...]
#     forbidden_words: Optional[...]


@router.get("/", response_class=HTMLResponse)
def settings_page(
    request: Request,
    peer_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    settings = (
        Setting.select()
        .join(Peer)
        .where(Peer.id == peer_id)
        .order_by(Setting.category.desc())
    )

    forbidden_links = (
        ForbiddenLink.select()
        .join(Peer)
        .where(Peer.id == peer_id)
        .order_by(ForbiddenLink.id)
    )
    forbidden_hosts = (
        ForbiddenHost.select()
        .join(Peer)
        .where(Peer.id == peer_id)
        .order_by(ForbiddenHost.id)
    )
    forbidden_words = (
        ForbiddenWord.select()
        .join(Peer)
        .where(Peer.id == peer_id)
        .order_by(ForbiddenWord.id)
    )

    context = {
        "title": "Очередь",
        "authenticated": authenticated,
        "project": configs.project_name,
        "request": request,
        "peer_id": peer_id,
        "settings": settings,
        "forbidden_links": forbidden_links,
        "forbidden_hosts": forbidden_hosts,
        "forbidden_words": forbidden_words,
    }

    return templates.TemplateResponse("settings.html", context)


@router.patch("/")
def update_seetings(
    request: Request,
    peer_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    return {"message": "Steeings updated"}
