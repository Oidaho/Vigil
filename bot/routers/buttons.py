from typing import Dict

from src.context import Context
from src.keyboards import EmptyKeyboard
from src.keyboards.answers import ShowSnackbar
from src.routers import ButtonRouter

from db.models import Conversation

from .utils import select_conversation

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
    conversation = (
        Conversation.select().where(Conversation.peer_id == ctx.peer.id).get_or_none()
    )

    if conversation is None:
        mark = payload.get("mark")
        new_marked = Conversation(peer_id=ctx.peer.id, name=ctx.peer.name, mark=mark)
        new_marked.save()
        snackbar_message = f'📝 Беседа помечена как "{mark}".'

    else:
        mark = conversation.mark
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
    conversation = (
        Conversation.select().where(Conversation.peer_id == ctx.peer.id).get_or_none()
    )

    if conversation is not None:
        mark = conversation.mark
        conversation.delete()
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
    conversation = (
        Conversation.select().where(Conversation.peer_id == ctx.peer.id).get_or_none()
    )

    if conversation is not None:
        conversation.peer_id = ctx.peer.id
        conversation.name = ctx.peer.name
        conversation.save()
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


@router.register(name="punish_in", check_owner=True)
def punish_in_button(ctx: Context, payload: Dict[str, int | str]) -> bool:
    text, keyboard = select_conversation(
        ctx=ctx,
        punishment=payload["punishment"],
        additionals={
            "target_user": payload["target_user"],
            "target_msg": payload["target_msg"],
            "reason": "Нарушение в чате.",
        },
    )

    ctx.api.messages.edit(
        peer_id=ctx.peer.id,
        cmid=ctx.button.cmid,
        message=text,
        keyboard=keyboard.json_str(),
    )

    snackbar_message = "🧑‍⚖️ Наказание выбрано."
    ctx.api.messages.sendMessageEventAnswer(
        event_id=ctx.button.id,
        user_id=ctx.user.id,
        peer_id=ctx.peer.id,
        event_data=ShowSnackbar(snackbar_message).json_str(),
    )

    return True


@router.register(name="execute_punishment", check_owner=True)
def execute_punishment_button(ctx: Context, payload: Dict[str, int | str]) -> bool:
    text = (
        f"[id{payload['target_user']}| Пользователь] был наказан.\n "
        f"Беседа: {payload['peer_name']}\n "
        f"Наказание: {payload['punishment']}\n "
        f"Причина: {payload['reason']}"
    )
    keyboard = EmptyKeyboard()
    ctx.api.messages.edit(
        peer_id=ctx.peer.id,
        cmid=ctx.button.cmid,
        message=text,
        keyboard=keyboard.json_str(),
    )

    match payload["punishment"]:
        case "unwarn":
            pass
        case "delete":
            pass
        case "warn":
            pass
        case "kick":
            pass

        case _:
            return False

    # TODO: Уведомить пользователя в чате
    return True
