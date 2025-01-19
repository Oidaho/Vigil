from src.routers import Rule
from src.context import Context

from db.models import Peer, Staff


class FromChatOnly(Rule):
    """Checks if the peer is marked with a specific label."""

    def check(self, ctx: Context) -> bool:
        peer = Peer.get_or_none(Peer.id == ctx.peer.id)
        if peer is None or (peer.mark != "CHAT"):
            return False

        return True


class IgnorePermitted(Rule):
    """Checks if the user who invoked the command has the required permission level."""

    def check(self, ctx: Context) -> bool:
        user = Staff.get_or_none(Staff.id == ctx.user.id)
        if user:
            return False

        return True
