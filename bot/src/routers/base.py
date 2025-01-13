from typing import Callable, Dict, List

from ..context import EventType, Context
from .rules import Rule


class Router:
    handlers: Dict[str, Callable] = {}
    bounded_type: EventType = None

    def __init__(self, ruleset: List[Rule]) -> None:
        self.ruleset = ruleset

    def check_rules(self, ctx: Context) -> None:
        for rule in self.ruleset:
            rule(ctx=ctx)
