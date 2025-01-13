from typing import List

from ..context import EventType
from .base import Router
from .rules import Rule


# TODO: write me
class MessageRouter(Router):
    """The router class for MESSAGE type events.

    Bounded type:
        EventType.MESSAGE
    """

    def __init__(self, routing_ruleset: List[Rule] = []) -> None:
        super().__init__(ruleset=routing_ruleset)
        self.bounded_type = EventType.MESSAGE
