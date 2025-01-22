import re
from typing import Dict, Tuple, NamedTuple

from src.context import Context
from src.keyboards import ButtonColor, EmptyKeyboard, Keyboard
from src.keyboards.actions import Callback

from db.models import Peer, Sanction

from config import configs


def exec_punishment(ctx: Context, punishment: str, args: NamedTuple) -> bool:
    target_user = extract_id(args.user_tag)

    if target_user is None:
        return False

    additionals = {
        "target_user": target_user,
    }

    if punishment != "unwarn":
        additionals.update({"reason": args.reason})

    text, keyboard = select_conversation(
        ctx=ctx,
        punishment=punishment,
        additionals=additionals,
    )

    ctx.api.messages.send(
        peer_ids=ctx.peer.id,
        random_id=0,
        message=text,
        keyboard=keyboard.json_str(),
    )

    return True


def select_conversation(
    ctx: Context, punishment: str, additionals: Dict[str, int | str]
) -> Tuple[str, Keyboard]:
    peers = Peer.select().where(Peer.mark == "CHAT")

    if not peers:
        text = "❗ У вас еще нет бесед, помеченных как 'CHAT'."
        keyboard = EmptyKeyboard()

    else:
        text = "❗ Выберите беседу, в которой необходимо произвести действие:"
        keyboard = Keyboard(inline=True, one_time=False, owner_id=ctx.user.id).add_row()
        for i, peer in enumerate(peers):
            if i % 2 == 0 and i != 0:
                keyboard.add_row()

            payload = {
                "punishment": punishment,
                "peer_id": peer.id,
                "peer_name": peer.name,
            }
            payload.update(additionals)

            keyboard.add_button(
                "execute_punishment",
                Callback(
                    label=peer.name,
                    payload=payload,
                ),
                ButtonColor.PRIMARY,
            )

        keyboard.add_row().add_button(
            "close",
            Callback(label="Закрыть"),
            ButtonColor.SECONDARY,
        )

    return text, keyboard


def extract_id(user_tag: str) -> int | None:
    pattern = r"^\[id[-+]?\d+\|\@?.*\]"
    if bool(re.findall(pattern, user_tag)):
        sep_pos = user_tag.find("|")
        return int(user_tag[3:sep_pos])
    else:
        return None


def execute_delete(ctx: Context, payload: Dict[str, int | str]) -> bool:
    target = payload["target_user"]
    target_msg = payload["target_msg"]
    peer_id = payload["peer_id"]
    ctx.api.messages.delete(
        cmids=target_msg,
        peer_id=peer_id,
        delete_for_all=1,
    )

    text = (
        f"Сообщение [id{target}|пользователя] удалено.\n"
        f"Причина: {payload['reason']}\n"
        f"Беседа: {payload['peer_name']}\n"
    )
    keyboard = EmptyKeyboard()
    ctx.api.messages.edit(
        peer_id=ctx.peer.id,
        cmid=ctx.button.cmid,
        message=text,
        keyboard=keyboard.json_str(),
    )

    return True


def execute_unwarn(ctx: Context, payload: Dict[str, int | str]) -> bool:
    user_id = payload["target_user"]
    peer_id = payload["peer_id"]

    sanction = (
        Sanction.select()
        .join(Peer)
        .where((Peer.id == peer_id) & (Sanction.user_id == user_id))
        .get_or_none()
    )

    if sanction is not None:
        sanction.points -= 1
        if sanction.points <= 0:
            sanction.delete_instance()

        else:
            sanction.save()

        text = (
            f"[id{user_id}|Пользователь] реабилитирован.\n"
            f"Предупреждения: {sanction.points}/{configs.bot.max_sanction_points}\n"
        )
        ctx.api.messages.send(
            peer_ids=peer_id,
            random_id=0,
            message=text,
        )

        text += f"Беседа: {payload['peer_name']}\n"
        keyboard = EmptyKeyboard()
        ctx.api.messages.edit(
            peer_id=ctx.peer.id,
            cmid=ctx.button.cmid,
            message=text,
            keyboard=keyboard.json_str(),
        )

    return True


def execute_warn(ctx: Context, payload: Dict[str, int | str]) -> int:
    user_id = payload["target_user"]
    peer_id = payload["peer_id"]
    kick = False

    peer = Peer.get_or_none(Peer.id == peer_id)
    sanction, created = Sanction.get_or_create(
        peer=peer,
        user_id=user_id,
        defaults={"peer": Peer.get(Peer.id == peer_id), "user_id": user_id},
    )

    text = f"[id{user_id}|Пользователь] получил предупреждение.\n"
    if not created:
        sanction.points += 1
        if sanction.points >= configs.bot.max_sanction_points:
            sanction.delete_instance()
            kick = True
            text = f"[id{payload['target_user']}|Пользователь] исключен, получив много предупреждений.\n"

        else:
            sanction.save()

    text += (
        f"Причина: {payload['reason']}\n"
        f"Предупреждения: {sanction.points}/{configs.bot.max_sanction_points}\n"
    )
    ctx.api.messages.send(
        peer_ids=peer_id,
        random_id=0,
        message=text,
    )

    text += f"Беседа: {payload['peer_name']}\n"
    keyboard = EmptyKeyboard()
    ctx.api.messages.edit(
        peer_id=ctx.peer.id,
        cmid=ctx.button.cmid,
        message=text,
        keyboard=keyboard.json_str(),
    )

    if kick:
        ctx.api.messages.removeChatUser(
            chat_id=peer_id - int(2e9),
            user_id=user_id,
        )

    return True


def execute_kick(ctx: Context, payload: Dict[str, int | str]) -> None:
    user_id = payload["target_user"]
    peer_id = payload["peer_id"]

    text = f"[id{user_id}|Пользователь] исключен.\nПричина: {payload['reason']}\n"
    ctx.api.messages.send(
        peer_ids=peer_id,
        random_id=0,
        message=text,
    )

    text += f"Беседа: {payload['peer_name']}\n"
    keyboard = EmptyKeyboard()
    ctx.api.messages.edit(
        peer_id=ctx.peer.id,
        cmid=ctx.button.cmid,
        message=text,
        keyboard=keyboard.json_str(),
    )

    ctx.api.messages.removeChatUser(
        chat_id=peer_id - int(2e9),
        user_id=user_id,
    )


def execute_conditional_warning(ctx: Context, reason: str) -> None:
    user_id = ctx.user.id
    peer_id = ctx.peer.id
    cmid = ctx.message.cmid

    peer = Peer.get_or_none(Peer.id == peer_id)
    sanction, created = Sanction.get_or_create(
        peer=peer,
        user_id=user_id,
        defaults={
            "peer": Peer.get(Peer.id == peer_id),
            "user_id": user_id,
            "points": 0,
        },
    )

    kick = False
    if created:
        text = (
            f"[id{user_id}|Пользователь] получил условное предупреждение.\n"
            f"Причина: {reason}\n"
        )

    else:
        sanction.points += 1
        text = (
            f"[id{user_id}|Пользователь] получил предупреждение.\n"
            f"Причина: {reason}\n"
            f"Предупреждения: {sanction.points}/{configs.bot.max_sanction_points}\n"
        )

        if sanction.points >= configs.bot.max_sanction_points:
            sanction.delete_instance()
            kick = True
            text = (
                f"[id{user_id}|Пользователь] исключен, получив много предупреждений.\n"
                f"Причина: {reason}\n"
                f"Предупреждения: {sanction.points}/{configs.bot.max_sanction_points}\n"
            )

        else:
            sanction.save()

    ctx.api.messages.delete(
        cmids=cmid,
        peer_id=peer_id,
        delete_for_all=1,
    )

    ctx.api.messages.send(
        peer_ids=peer_id,
        random_id=0,
        message=text,
    )

    log_chats = Peer.select().where(Peer.mark == "LOG")
    log_peer_ids = [item.id for item in log_chats]

    text += f"Беседа: {ctx.peer.name}\n"
    ctx.api.messages.send(
        peer_ids=log_peer_ids,
        random_id=0,
        message=text,
    )

    if kick:
        ctx.api.messages.removeChatUser(
            chat_id=peer_id - int(2e9),
            user_id=user_id,
        )


def quiet_delete(ctx: Context) -> None:
    peer_id = ctx.peer.id
    cmid = ctx.message.cmid

    ctx.api.messages.delete(
        cmids=cmid,
        peer_id=peer_id,
        delete_for_all=1,
    )
