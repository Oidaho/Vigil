"""The `reactions` module provides tools for routing events of type REACTION.

Classes:
    - `ReactionRouter`: A router class.
"""

from typing import List

from ..context import EventType
from .base import Router
from .rules import Rule


class ReactionRouter(Router):
    """A router class for handling events of type REACTION.

    Bounded Event Type:
        EventType.REACTION
    """

    def __init__(self, routing_ruleset: List[Rule] = []) -> None:
        self.ruleset = routing_ruleset
        self.bounded_type = EventType.Reaction
        self.handlers = {}
