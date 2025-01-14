import re
from typing import Dict, Tuple, NamedTuple

from src.context import Context
from src.keyboards import ButtonColor, EmptyKeyboard, Keyboard
from src.keyboards.actions import Callback

from db.models import Conversation


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
        text = "❗ Выберите беседу, в которой необходимо наказать пользователя:"
        keyboard = Keyboard(inline=True, one_time=False, owner_id=ctx.user.id).add_row()
        for conversation in conversations:
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

    return text, keyboard


def extract_id(user_tag: str) -> int | None:
    pattern = r"^\[id[-+]?\d+\|\@?.*\]"
    if bool(re.findall(pattern, user_tag)):
        sep_pos = user_tag.find("|")
        return int(user_tag[3:sep_pos])
    else:
        return None
