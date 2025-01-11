from ..context import EventType
from .base import Router


# TODO: write me
class MessageRouter(Router):
    """The router class for MESSAGE type events.

    Bounded type:
        EventType.MESSAGE
    """

    def __init__(self) -> None:
        self.bounded_type = EventType.MESSAGE
