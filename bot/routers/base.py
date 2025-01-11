from typing import Callable, Dict

from ..context import EventType


class Router:
    handlers: Dict[str, Callable] = {}
    bounded_type: EventType = None
