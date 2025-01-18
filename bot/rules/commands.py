from src.routers import Rule
from src.context import Context

from db.models import Peer


class FromMarkedOnly(Rule):
    """Checks if the peer is marked with a specific label."""

    def __init__(self, mark: str) -> None:
        self.mark = mark

    def check(self, ctx: Context) -> bool:
        peer = Peer.get_or_none(Peer.id == ctx.peer.id)
        if peer is None or (peer.mark != self.mark):
            return False

        return True


class ReplyRequired(Rule):
    """Makes the presence of a reply message in the event mandatory."""

    def check(self, ctx: Context) -> bool:
        if ctx.message.reply:
            return True

        return False


class ForwardRequired(Rule):
    """Makes the presence of a forwarded messages in the event mandatory."""

    def __init__(self, msg_count: int) -> None:
        self.count = msg_count

    def check(self, ctx: Context) -> bool:
        if len(ctx.message.forward) == self.count:
            return True

        return False
