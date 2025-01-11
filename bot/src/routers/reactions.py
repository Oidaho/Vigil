from ..context import EventType
from .base import Router


class ReactionRouter(Router):
    """The router class for REACTION type events.

    Bounded type:
        EventType.REACTION
    """

    def __init__(self) -> None:
        self.bounded_type = EventType.REACTION
