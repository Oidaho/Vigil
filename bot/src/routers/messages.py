"""The `messages` module provides tools for routing events of type MESSAGE.

Classes:
    - `MessageRouter`: A router class.
"""

from typing import List
from functools import wraps

from ..context import Context, EventType
from .base import Router
from .rules import Rule

from loguru import logger


# TODO: write me
class MessageRouter(Router):
    """A router class for handling events of type MESSAGE.

    Bounded Event Type:
        EventType.MESSAGE
    """

    def __init__(self, routing_ruleset: List[Rule] = []) -> None:
        self.ruleset = routing_ruleset
        self.bounded_type = EventType.MESSAGE
        self.handlers = {}

    def route(self, context: Context) -> None:
        """Extracts the name of the executed command from the context of a COMMAND-type event,
        which is used for routing and initiating specific response actions by calling
        the corresponding command handler.

        Args:
            context (Context): The event context.

        Raises:
            RuntimeError: Routing deadlock. The command handler was not found.
        """
        self.check_rules(context)

        for name, handler in self.handlers.items():
            try:
                triggered = handler(context)
                if triggered:
                    logger.info(
                        f"The triggering of the handler '{name}' has stopped the execution of other handlers."
                    )
                    break

            except Exception as error:
                logger.error(
                    f"An error occurred while executing the message handler: {error}."
                )

    def register(
        self,
        name: str = None,
        execution_ruleset: List[Rule] = [],
    ) -> None:
        """A decorator that registers a new message handler and assigns it a name.
        Handler functions marked with this decorator must include the required arguments:
        `ctx` and `msg`.

        Args:
            name (str, optional): The name of the button. If not specified,
                                the name of the handler function will be used.
                                Defaults to None.
            execution_ruleset (List[Rule], optional): A list of rules that must be validated
                                        before executing the message handler.

        Example:
            ```python
            router = MessageRouter()

            @router.register(name='trashtalk')
            def check_trashtalk(ctx, msg) -> bool:
                # Response actions here
                return True
            ```
        """

        def decorator(func):
            @wraps(func)
            def wrapper(context: Context):
                for rule in execution_ruleset:
                    rule(context)

                # In fact, it's just a shortcut
                message = context.message

                result = func(ctx=context, msg=message)
                logger.info(
                    f"The event triggered the execution of the message handler '{name}'."
                )

                return result

            self.handlers[name if name else func.__name__] = wrapper
            return wrapper

        return decorator
