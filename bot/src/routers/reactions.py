from typing import List

from ..context import EventType
from .base import Router
from .rules import Rule


class ReactionRouter(Router):
    """The router class for REACTION type events.

    Bounded type:
        EventType.REACTION
    """

    def __init__(self, routing_ruleset: List[Rule] = []) -> None:
        super().__init__(ruleset=routing_ruleset)
        self.bounded_type = EventType.REACTION
