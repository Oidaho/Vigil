from auth import AuthData, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import configs
from db.models import Peer, Sanction

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/{peer_id}/sanctions")


@router.get("/", response_class=HTMLResponse)
def sanctions_page(
    request: Request,
    peer_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    peer = Peer.get_or_none(Peer.id == peer_id)
    if peer:
        sanctions = (
            Sanction.select().where(Sanction.peer == peer).order_by(Sanction.user_id)
        )

        context = {
            "title": "Санкции",
            "authenticated": authenticated,
            "project": configs.PROJECT_NAME,
            "sanctions": sanctions,
            "request": request,
            "peer_id": peer_id,
            "peer_name": peer.name,
            "max_sanction_points": configs.bot.MAX_SANCTION_POINTS,
        }

        return templates.TemplateResponse("sanctions.html", context)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No peer with this ID was found.",
    )


@router.delete("/{user_id}")
def delete_sanction(
    peer_id: int,
    user_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    sanction = (
        Sanction.select()
        .join(Peer)
        .where((Peer.id == peer_id) & (Sanction.user_id == user_id))
        .get_or_none()
    )
    if sanction:
        sanction.delete_instance()
        return {"message": "The sanction has been removed."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No sanction or peer with this ID was found.",
    )


@router.patch("/{user_id}")
def decrement_sanction(
    peer_id: int,
    user_id: int,
    authenticated: AuthData = Depends(get_current_user),
):
    sanction = (
        Sanction.select()
        .join(Peer)
        .where((Peer.id == peer_id) & (Sanction.user_id == user_id))
        .get_or_none()
    )
    if sanction:
        sanction.points -= 1
        if sanction.points <= 0:
            sanction.delete_instance()
            return {"message": "The sanction has been removed."}

        sanction.save()
        return {"message": "The sanction has been decremented."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No sanction or peer with this ID was found.",
    )
