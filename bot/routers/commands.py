from typing import NamedTuple

from rules.commands import ForwardRequired, FromMarkedOnly, PermissionRequired
from src.context import Context
from src.keyboards import ButtonColor, Keyboard
from src.keyboards.actions import Callback
from src.routers import CommandRouter

from db.models import Peer, Staff

from .utils import exec_punishment

router = CommandRouter()


@router.register(
    name="health",
    args=(),
    execution_ruleset=[
        PermissionRequired(min_permission=1),
        FromMarkedOnly(mark="LOG"),
    ],
)
def health_command(ctx: Context, args: NamedTuple) -> bool:
    user = Staff.get_or_none(Staff.id == ctx.user.id)
    if user:
        permission = user.permission
        text = f"[id{ctx.user.id}|{ctx.user.first_name}], я в порядке!\n Ваш уровень прав: {permission}\n"
        if permission >= 2:
            text += "Вам доступен вход в веб-панель: https://stalcraft-funcka.ru/"

        ctx.api.messages.send(
            peer_ids=ctx.peer.id,
            random_id=0,
            message=text,
        )

        return True

    return False


@router.register(
    name="mark",
    args=(),
    execution_ruleset=[
        PermissionRequired(min_permission=2),
    ],
)
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
    execution_ruleset=[
        PermissionRequired(min_permission=1),
        FromMarkedOnly(mark="LOG"),
    ],
)
def kick_command(ctx: Context, args: NamedTuple) -> bool:
    return exec_punishment(ctx=ctx, punishment="kick", args=args)


@router.register(
    name="warn",
    args=("user_tag", "reason"),
    execution_ruleset=[
        PermissionRequired(min_permission=1),
        FromMarkedOnly(mark="LOG"),
    ],
)
def warn_command(ctx: Context, args: NamedTuple) -> bool:
    return exec_punishment(ctx=ctx, punishment="warn", args=args)


@router.register(
    name="unwarn",
    args=("user_tag",),
    execution_ruleset=[
        PermissionRequired(min_permission=1),
        FromMarkedOnly(mark="LOG"),
    ],
)
def unwarn_command(ctx: Context, args: NamedTuple) -> bool:
    return exec_punishment(ctx=ctx, punishment="unwarn", args=args)


@router.register(
    name="punish",
    args=(),
    execution_ruleset=[
        PermissionRequired(min_permission=1),
        FromMarkedOnly(mark="LOG"),
        ForwardRequired(msg_count=1),
    ],
    delete_src=False,
)
def punish_command(ctx: Context, args: NamedTuple) -> bool:
    target_user = ctx.message.forward[0].author
    target_msg = ctx.message.forward[0].cmid
    peer_id = ctx.message.forward[0].peer
    peer_name = Peer.get(Peer.id == peer_id).name

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
            "execute_punishment",
            Callback(
                label=label,
                payload={
                    "punishment": punishment,
                    "target_user": target_user,
                    "target_msg": target_msg,
                    "peer_id": peer_id,
                    "peer_name": peer_name,
                    "reason": "Нарушение в чате.",
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
