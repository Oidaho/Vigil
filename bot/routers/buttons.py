from typing import Dict

from src.context import Context
from src.keyboards.answers import ShowSnackbar
from src.routers import ButtonRouter

from db.models import Peer

from .utils import (
    execute_kick,
    execute_delete,
    execute_unwarn,
    execute_warn,
)

router = ButtonRouter()


@router.register(name="close", check_owner=True)
def close_button(ctx: Context, payload: Dict[str, int | str]) -> bool:
    ctx.api.messages.delete(
        peer_id=ctx.peer.id,
        cmids=ctx.button.cmid,
        delete_for_all=1,
    )

    ctx.api.messages.sendMessageEventAnswer(
        event_id=ctx.button.id,
        user_id=ctx.user.id,
        peer_id=ctx.peer.id,
        event_data=ShowSnackbar("❌ Закрыто.").json_str(),
    )

    return True


@router.register(name="set_mark", check_owner=True)
def set_mark_button(ctx: Context, payload: Dict[str, int | str]) -> bool:
    mark = payload.get("mark")
    peer, created = Peer.get_or_create(
        id=ctx.peer.id,
        defaults={
            "id": ctx.peer.id,
            "name": ctx.peer.name,
            "mark": mark,
        },
    )

    mark = peer.mark
    if created:
        snackbar_message = f'📝 Беседа помечена как "{mark}".'

    else:
        snackbar_message = f'❗Беседа уже имеет метку "{mark}".'

    ctx.api.messages.sendMessageEventAnswer(
        event_id=ctx.button.id,
        user_id=ctx.user.id,
        peer_id=ctx.peer.id,
        event_data=ShowSnackbar(snackbar_message).json_str(),
    )

    return True


@router.register(name="drop_mark", check_owner=True)
def drop_mark_button(ctx: Context, payload: Dict[str, int | str]) -> bool:
    peer = Peer.get_or_none(Peer.id == ctx.peer.id)

    if peer is not None:
        mark = peer.mark
        peer.delete_instance()
        snackbar_message = f'📝 Метка "{mark}" снята с беседы.'

    else:
        snackbar_message = "❗Беседа еще не имеет метку."

    ctx.api.messages.sendMessageEventAnswer(
        event_id=ctx.button.id,
        user_id=ctx.user.id,
        peer_id=ctx.peer.id,
        event_data=ShowSnackbar(snackbar_message).json_str(),
    )

    return True


@router.register(name="update_conversation", check_owner=True)
def update_conversation_button(ctx: Context, payload: Dict[str, int | str]) -> bool:
    peer = Peer.get_or_none(Peer.peer_id == ctx.peer.id)

    if peer is not None:
        peer.id = ctx.peer.id
        peer.name = ctx.peer.name
        peer.save()
        snackbar_message = "📝 Данные беседы обновлены."

    else:
        snackbar_message = "❗Беседа еще не имеет метку."

    ctx.api.messages.sendMessageEventAnswer(
        event_id=ctx.button.id,
        user_id=ctx.user.id,
        peer_id=ctx.peer.id,
        event_data=ShowSnackbar(snackbar_message).json_str(),
    )

    return True


@router.register(name="execute_punishment", check_owner=True)
def execute_punishment_button(ctx: Context, payload: Dict[str, int | str]) -> bool:
    punishments = {
        "kick": execute_kick,
        "warn": execute_warn,
        "unwarn": execute_unwarn,
        "delete": execute_delete,
    }

    func = punishments.get(payload["punishment"])
    if func is not None:
        snackbar_message = "🧑‍⚖️ Наказание выбрано."
        ctx.api.messages.sendMessageEventAnswer(
            event_id=ctx.button.id,
            user_id=ctx.user.id,
            peer_id=ctx.peer.id,
            event_data=ShowSnackbar(snackbar_message).json_str(),
        )

        return func(ctx, payload)

    return False
