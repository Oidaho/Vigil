from bot.routers import Commands
from bot.context import Context
from typing import NamedTuple


router = Commands()


@router.register(name="test", args=())
def test_command(ctx: Context, args: NamedTuple) -> None:
    ctx.api.messages.send(peer_id=ctx.peer.id, message="Test command!")
