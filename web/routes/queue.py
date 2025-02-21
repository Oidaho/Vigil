from datetime import datetime

from auth import AuthData, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import configs
from db.models import Peer, Queue

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/{peer_id}/queue")


@router.get("/", response_class=HTMLResponse)
def queue_page(
    request: Request,
    peer_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    peer = Peer.get_or_none(Peer.id == peer_id)
    if peer:
        queue = (
            Queue.select().where(Queue.peer == peer).order_by(Queue.expiration.desc())
        )

        context = {
            "title": "Очередь",
            "authenticated": authenticated,
            "project": configs.PROJECT_NAME,
            "queue": queue,
            "request": request,
            "peer_id": peer_id,
            "peer_name": peer.name,
            "now": datetime.utcnow(),
        }

        return templates.TemplateResponse("queue.html", context)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No peer with this ID was found.",
    )


@router.delete("/{user_id}")
def delete_queue_item(
    peer_id: int,
    user_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    queue_item = (
        Queue.select()
        .join(Peer)
        .where((Peer.id == peer_id) & (Queue.user_id == user_id))
        .get_or_none()
    )
    if queue_item:
        queue_item.delete_instance()
        return {"message": "The queue item has been removed."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No peer with this ID was found.",
    )
