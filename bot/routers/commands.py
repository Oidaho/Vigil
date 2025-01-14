from typing import NamedTuple

from rules.commands import FromMarkedOnly, ForwardRequired
from src.context import Context
from src.keyboards import ButtonColor, Keyboard
from src.keyboards.actions import Callback
from src.routers import CommandRouter

from .utils import exec_punishment

router = CommandRouter()


@router.register(name="mark", args=(), execution_ruleset=[])
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
            "update_conversation",
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
            ButtonColor.SECONDARY,
        )
    )

    ctx.api.messages.send(
        peer_ids=ctx.peer.id,
        random_id=0,
        message=text,
        keyboard=keyboard.json_str(),
    )

    return True


@router.register(
    name="kick",
    args=("user_tag", "reason"),
    execution_ruleset=[FromMarkedOnly(mark="LOG")],
)
def kick_command(ctx: Context, args: NamedTuple) -> bool:
    return exec_punishment(ctx=ctx, punishment="kick", args=args)


@router.register(
    name="warn",
    args=("user_tag", "reason"),
    execution_ruleset=[FromMarkedOnly(mark="LOG")],
)
def warn_command(ctx: Context, args: NamedTuple) -> bool:
    return exec_punishment(ctx=ctx, punishment="warn", args=args)


@router.register(
    name="unwarn",
    args=("user_tag", "reason"),
    execution_ruleset=[FromMarkedOnly(mark="LOG")],
)
def unwarn_command(ctx: Context, args: NamedTuple) -> bool:
    return exec_punishment(ctx=ctx, punishment="unwarn", args=args)


@router.register(
    name="punish",
    args=(),
    execution_ruleset=[
        FromMarkedOnly(mark="LOG"),
        ForwardRequired(msg_count=1),
    ],
)
def punish_command(ctx: Context, args: NamedTuple) -> bool:
    target = ctx.message.forward[0].author

    text = (
        "❓ Как вы хотите наказать пользователя? \n\n"
        "Выберите необходимое дествие из меню ниже:"
    )

    keyboard = Keyboard(inline=True, one_time=False, owner_id=ctx.user.id).add_row()

    pinushments = (
        ("Удалить сообщение", "delete", ButtonColor.PRIMARY),
        ("Предупредить", "warn", ButtonColor.PRIMARY),
        ("Выгнать", "kick", ButtonColor.NEGATIVE),
    )
    for label, punishment, color in pinushments:
        keyboard.add_button(
            "punish_in",
            Callback(
                label=label,
                payload={
                    "punishment": punishment,
                    "target": target,
                },
            ),
            color,
        )

    keyboard.add_row().add_button(
        "close",
        Callback(label="Закрыть"),
        ButtonColor.SECONDARY,
    )

    ctx.api.messages.send(
        peer_ids=ctx.peer.id,
        random_id=0,
        message=text,
        keyboard=keyboard.json_str(),
    )

    return True
