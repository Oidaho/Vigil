from bot.routers import Commands
from bot.context import Context
from typing import NamedTuple


router = Commands()


@router.register(name="test", args=())
def test_command(ctx: Context, args: NamedTuple) -> None:
    ctx.api.messages.send(peer_id=ctx.peer.id, message="Test command!", random_id=0)


@router.register(name="test2", args=("arg1", "arg2"))
def test2_command(ctx: Context, args: NamedTuple) -> None:
    ctx.api.messages.send(
        peer_id=ctx.peer.id, message=f"Test command with args <{args}>!", random_id=0
    )
