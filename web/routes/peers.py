from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import AuthData, get_current_user
from config import configs
from db.models import Peer

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/peers")


@router.get("/", response_class=HTMLResponse)
def peers_page(
    request: Request,
    authenticated: AuthData = Depends(get_current_user),
):
    peers = Peer.select().order_by(Peer.mark)

    context = {
        "title": "Чаты",
        "authenticated": authenticated,
        "project": configs.project_name,
        "peers": peers,
        "request": request,
    }

    return templates.TemplateResponse("peers.html", context)


@router.delete("/{peer_id}")
def unmark_peer(
    peer_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    peer = Peer.get_or_none(Peer.id == peer_id)
    if peer:
        peer.delete_instance()
        return {"message": "Peer mark has been removed"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such peer was found"
    )
