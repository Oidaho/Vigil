from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import AuthData, get_current_user
from config import configs
from db.models import ForbiddenHost, ForbiddenLink, ForbiddenWord, Peer, Setting

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/{peer_id}/settings")


@router.get("/", response_class=HTMLResponse)
def settings_page(
    request: Request,
    peer_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    peer = Peer.get_or_none(Peer.id == peer_id)
    if peer:
        settings = (
            Setting.select()
            .where(Setting.peer == peer)
            .order_by(Setting.category.desc())
        )
        forbidden_links = (
            ForbiddenLink.select()
            .where(ForbiddenLink.peer == peer)
            .order_by(ForbiddenLink.id)
        )
        forbidden_hosts = (
            ForbiddenHost.select()
            .where(ForbiddenHost.peer == peer)
            .order_by(ForbiddenHost.id)
        )
        forbidden_words = (
            ForbiddenWord.select()
            .where(ForbiddenWord.peer == peer)
            .order_by(ForbiddenWord.id)
        )

        context = {
            "title": "Настройки",
            "authenticated": authenticated,
            "project": configs.project_name,
            "request": request,
            "peer_id": peer_id,
            "peer_name": peer.name,
            "settings": settings,
            "forbidden_links": forbidden_links,
            "forbidden_hosts": forbidden_hosts,
            "forbidden_words": forbidden_words,
        }

        return templates.TemplateResponse("settings.html", context)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such peer was found"
    )


@router.patch("/")
def update_seetings(
    request: Request,
    peer_id: int,
    updated_settings: list = Body(...),
    authenticated: AuthData = Depends(get_current_user),
):
    peer = Peer.get_or_none(Peer.id == peer_id)
    if peer:
        for setting_data in updated_settings:
            setting = Setting.get_or_none(
                (Setting.peer == peer) & (Setting.key == setting_data["key"])
            )
            if setting:
                setting.value = setting_data["value"]
                setting.save()

        return {"message": "Settings updated"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such peer was found"
    )


@router.post("/words")
def add_forbidden_word(
    request: Request,
    peer_id: int,
    item_value: str = Body(...),
    authenticated: AuthData = Depends(get_current_user),
):
    peer = Peer.get_or_none(Peer.id == peer_id)
    if peer:
        ForbiddenWord.create(peer=peer, value=item_value)
        return {"message": "Word created"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such peer was found"
    )


@router.delete("/words/{item_id}")
def delete_forbidden_word(
    request: Request,
    peer_id: int,
    item_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    word = (
        ForbiddenWord.select()
        .join(Peer)
        .where((Peer.id == peer_id) & (ForbiddenWord.id == item_id))
        .get_or_none()
    )
    if word:
        word.delete_instance()
        return {"message": "Word has been removed"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such word was found"
    )


@router.post("/links")
def add_forbidden_link(
    request: Request,
    peer_id: int,
    item_value: str = Body(...),
    authenticated: AuthData = Depends(get_current_user),
):
    peer = Peer.get_or_none(Peer.id == peer_id)
    if peer:
        ForbiddenLink.create(peer=peer, value=item_value)
        return {"message": "Link created"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such peer was found"
    )


@router.delete("/links/{item_id}")
def delete_forbidden_link(
    request: Request,
    peer_id: int,
    item_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    link = (
        ForbiddenLink.select()
        .join(Peer)
        .where((Peer.id == peer_id) & (ForbiddenLink.id == item_id))
        .get_or_none()
    )
    if link:
        link.delete_instance()
        return {"message": "Link has been removed"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such link was found"
    )


@router.post("/hosts")
def add_forbidden_host(
    request: Request,
    peer_id: int,
    item_value: str = Body(...),
    authenticated: AuthData = Depends(get_current_user),
):
    peer = Peer.get_or_none(Peer.id == peer_id)
    if peer:
        ForbiddenHost.create(peer=peer, value=item_value)
        return {"message": "Host created"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such peer was found"
    )


@router.delete("/hosts/{item_id}")
def delete_forbidden_host(
    request: Request,
    peer_id: int,
    item_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    host = (
        ForbiddenHost.select()
        .join(Peer)
        .where((Peer.id == peer_id) & (ForbiddenHost.id == item_id))
        .get_or_none()
    )
    if host:
        host.delete_instance()
        return {"message": "Host has been removed"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such host was found"
    )
