"""The `messages` module provides tools for routing events of type MESSAGE.

Classes:
    - `MessageRouter`: A router class.
"""

from typing import List

from ..context import EventType
from .base import Router
from .rules import Rule


# TODO: write me
class MessageRouter(Router):
    """A router class for handling events of type MESSAGE.

    Bounded Event Type:
        EventType.MESSAGE
    """

    def __init__(self, routing_ruleset: List[Rule] = []) -> None:
        super().__init__(ruleset=routing_ruleset)
        self.bounded_type = EventType.MESSAGE
