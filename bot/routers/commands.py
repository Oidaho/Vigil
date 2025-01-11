from src.routers import CommandRouter
from src.context import Context
from typing import NamedTuple

from src.keyboards import Keyboard, ButtonColor
from src.keyboards.actions import Callback


router = CommandRouter()


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
            "set_mark",
            Callback(label="CHAT", payload={"mark": "CHAT"}),
            ButtonColor.POSITIVE,
        )
        .add_button(
            "set_mark",
            Callback(label="LOG", payload={"mark": "LOG"}),
            ButtonColor.POSITIVE,
        )
        .add_row()
        .add_button(
            "update_coversation",
            Callback(label="Обновить данные беседы"),
            ButtonColor.SECONDARY,
        )
        .add_row()
        .add_button(
            "drop_mark",
            Callback(label="Сбросить метку"),
            ButtonColor.NEGATIVE,
        )
        .add_button(
            "close",
            Callback(label="Закрыть"),
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
