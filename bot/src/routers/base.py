"""The `buttons` module provides tools for routing events.

Classes:
    - `Router`: A router class.
"""

from typing import Callable, Dict, List

from ..context import EventType, Context
from .rules import Rule


class Router:
    """Base router class."""

    handlers: Dict[str, Callable] = {}
    bounded_type: EventType = None

    def __init__(self, ruleset: List[Rule]) -> None:
        self.ruleset = ruleset

    def check_rules(self, ctx: Context) -> None:
        for rule in self.ruleset:
            rule(ctx=ctx)
