from src.routers import Rule
from src.context import Context

from db.models import Conversation


class FromMarkedOnly(Rule):
    def __init__(self, mark: str) -> None:
        self.mark = mark

    def check(self, ctx: Context) -> bool:
        conversation = (
            Conversation.select()
            .where(Conversation.peer_id == ctx.peer.id)
            .get_or_none()
        )

        if conversation is None or (conversation.mark != self.mark):
            return False

        return True


class ReplyRequired(Rule):
    def check(self, ctx: Context) -> bool:
        if ctx.message.reply:
            return True

        return False


class ForwardRequired(Rule):
    def __init__(self, msg_count: int) -> None:
        self.count = msg_count

    def check(self, ctx: Context) -> bool:
        if len(ctx.message.forward) == self.count:
            return True

        return False
