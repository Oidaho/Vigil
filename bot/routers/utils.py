import re
from typing import Dict, Tuple, NamedTuple

from src.context import Context
from src.keyboards import ButtonColor, EmptyKeyboard, Keyboard
from src.keyboards.actions import Callback

from db.models import Conversation, Sanction

from config import configs


def exec_punishment(ctx: Context, punishment: str, args: NamedTuple) -> bool:
    target_user = extract_id(args.user_tag)

    if target_user is None:
        return False

    text, keyboard = select_conversation(
        ctx=ctx,
        punishment=punishment,
        additionals={
            "target_user": target_user,
            "reason": args.reason,
        },
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
    conversations = Conversation.select().where(Conversation.mark == "CHAT")

    if not conversations:
        text = "❗ У вас еще нет бесед, помеченных как 'CHAT'."
        keyboard = EmptyKeyboard()

    else:
        text = "❗ Выберите беседу, в которой необходимо произвести действие:"
        keyboard = Keyboard(inline=True, one_time=False, owner_id=ctx.user.id).add_row()
        for i, conversation in enumerate(conversations):
            if i % 2 == 0 and i != 0:
                keyboard.add_row()

            payload = {
                "punishment": punishment,
                "peer_id": conversation.peer_id,
                "peer_name": conversation.name,
            }
            payload.update(additionals)

            keyboard.add_button(
                "execute_punishment",
                Callback(
                    label=conversation.name,
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
    target = payload["target_id"]
    peer_id = payload["peer_id"]

    conversation = Conversation.select().where(Conversation.peer_id == peer_id).get()
    sanction = (
        Sanction.select()
        .where((Sanction.conversation == conversation) & (Sanction.user_id == target))
        .get_or_none()
    )

    if sanction is not None:
        warns = sanction.warns_count - 1
        if warns <= 0:
            sanction.delete()

        else:
            sanction.warns_count = warns
            sanction.save()

        text = (
            f"[id{target}|Пользователь] реабилитирован.\n"
            f"Причина: {payload['reason']}\n"
            f"Предупреждения: {warns}/{configs.bot.max_warns}\n"
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
    target = payload["target_user"]
    peer_id = payload["peer_id"]
    kick = False

    conversation = Conversation.select().where(Conversation.peer_id == peer_id).get()
    sanction = (
        Sanction.select()
        .where((Sanction.conversation == conversation) & (Sanction.user_id == target))
        .get_or_none()
    )

    text = f"[id{target}|Пользователь] получил предупреждение.\n"
    if sanction is None:
        warns = 1
        new_sanction = Sanction(
            conversation=conversation,
            user_id=target,
            warns_count=warns,
        )
        new_sanction.save()

    else:
        sanction.warns_count += 1
        sanction.save()

        warns = sanction.warns_count
        if warns >= configs.bot.max_warns:
            sanction.delete()
            kick = True
            text = f"[id{payload['target_user']}|Пользователь] исключен, получив много предупреждений.\n"

    text += (
        f"Причина: {payload['reason']}\n"
        f"Предупреждения: {warns}/{configs.bot.max_warns}\n"
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
            user_id=target,
        )

    return True


def execute_kick(ctx: Context, payload: Dict[str, int | str]) -> None:
    target = payload["target_user"]
    peer_id = payload["peer_id"]

    text = f"[id{target}|Пользователь] исключен.\nПричина: {payload['reason']}\n"
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
        user_id=target,
    )
