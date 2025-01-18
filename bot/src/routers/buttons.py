"""The `buttons` module provides tools for routing events of type BUTTONS.

Classes:
    - `ButtonRouter`: A router class.
"""

from functools import wraps
from typing import List, Callable

from loguru import logger

from ..context import Context, EventType
from ..keyboards.answers import ShowSnackbar
from .base import Router
from .rules import Rule


def error_factory(text: str) -> Callable:
    def error_func(ctx: Context) -> bool:
        ctx.api.messages.sendMessageEventAnswer(
            event_id=ctx.button.id,
            user_id=ctx.user.id,
            peer_id=ctx.peer.id,
            event_data=ShowSnackbar(text).json_str(),
        )

        return True

    return error_func


class ButtonRouter(Router):
    """A router class for handling events of type BUTTON.

    Bounded Event Type:
        EventType.BUTTON
    """

    def __init__(self, routing_ruleset: List[Rule] = []) -> None:
        super().__init__(ruleset=routing_ruleset)
        self.bounded_type = EventType.BUTTON
        self.handlers["error"] = error_factory("⚠️ Что-то пошло не так.")
        self.handlers["rejected"] = error_factory("⚠️ Действие отклонено.")
        self.handlers["lack_permission"] = error_factory("⚠️ Недостаточно прав.")

    def route(self, context: Context) -> None:
        """Extracts the button name from the context of BUTTON-type events,
        which is used for routing and initiating specific response actions
        by calling the corresponding button handler.

        Args:
            context (Context): The event context.

        Raises:
            RuntimeError: Routing deadlock. The button handler was not found.
        """
        self.check_rules(context)

        name = context.button.payload.get("name")
        handler = self.handlers.get(name)

        try:
            if handler is None:
                raise NameError(f"Couldn't find a button handler named '{name}'.")

            return handler(context)

        except (RuntimeError, PermissionError) as error:
            if isinstance(error, RuntimeError):
                error_func = self.handlers.get("rejected")
            else:
                error_func = self.handlers.get("lack_permission")
            error_func(context)
            logger.warning(f"Button handler execution canceled: {error}")

        except Exception as error:
            error_func = self.handlers.get("error")
            error_func(context)
            logger.error(f"Error when executing button handler: {error}")

    def register(
        self,
        name: str = None,
        check_owner: bool = False,
        execution_ruleset: List[Rule] = [],
    ) -> None:
        """A decorator that registers a new button handler and assigns it a name.
        Handler functions marked with this decorator must include the required arguments:
        `ctx` and `payload`.

        Args:
            name (str, optional): The name of the button. If not specified,
                                the name of the handler function will be used.
                                Defaults to None.
            check_owner (bool, optional): Indicates whether to verify that the user
                                        who pressed the button is the owner of the
                                        keyboard attached to the message.
                                        Defaults to True.

        Example:
            ```python
            router = Buttons()

            @router.register(name='close')
            def close_button(ctx, payload) -> bool:
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
                payload = context.button.payload

                if check_owner and (context.user.id != payload["owner"]):
                    raise PermissionError(
                        f"User <{context.user.id}> is not button '{name}' owner."
                    )

                result = func(ctx=context, payload=payload)
                logger.info(f"Event triggered button handler '{name}' execution.")

                return result

            self.handlers[name if name else func.__name__] = wrapper
            return wrapper

        return decorator
