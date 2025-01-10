from bot.routers import Commands
from bot.context import Context
from typing import NamedTuple

from bot.keyboards import Keyboard, ButtonColor
from bot.keyboards.actions import Callback


router = Commands()


@router.register(name="mark", args=())
def mark_command(ctx: Context, args: NamedTuple) -> bool:
    text = (
        "⚠️ Вы хотите задать метку беседе? \n\n"
        "Выберите необходимое дествие из меню ниже:"
    )

    keyboard = (
        Keyboard(inline=True, one_time=False, owner_id=ctx.user.id)
        .add_row()
        .add_button(
            Callback(label="CHAT", payload={"call": "set_mark", "mark": "CHAT"}),
            ButtonColor.POSITIVE,
        )
        .add_button(
            Callback(label="LOG", payload={"call": "set_mark", "mark": "LOG"}),
            ButtonColor.POSITIVE,
        )
        .add_row()
        .add_button(
            Callback(
                label="Обновить данные беседы",
                payload={"call": "update_coversation"},
            ),
            ButtonColor.SECONDARY,
        )
        .add_row()
        .add_button(
            Callback(label="Сбросить метку", payload={"call": "drop_mark"}),
            ButtonColor.NEGATIVE,
        )
        .add_button(
            Callback(label="Закрыть", payload={"call": "cancel"}),
            ButtonColor.NEGATIVE,
        )
    )

    ctx.api.messages.send(
        peer_ids=ctx.peer.id,
        random_id=0,
        message=text,
        keyboard=keyboard.json_str(),
    )

    return True


@router.register(name="kick", args=("user_tag", "reason"))
def kick_command(ctx: Context, args: NamedTuple) -> bool:
    pass


@router.register(name="kick", args=("user_tag", "reason"))
def warn_command(ctx: Context, args: NamedTuple) -> bool:
    pass


@router.register(name="kick", args=("user_tag", "reason"))
def unwarn_command(ctx: Context, args: NamedTuple) -> bool:
    pass
