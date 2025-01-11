from functools import wraps
from typing import Dict

from loguru import logger

from ..context import Context, EventType
from ..keyboards.responds import ShowSnackbar
from .base import Router


def error(ctx: Context) -> bool:
    ctx.api.messages.sendMessageEventAnswer(
        event_id=ctx.button.id,
        user_id=ctx.user.id,
        peer_id=ctx.peer.id,
        event_data=ShowSnackbar("⚠️ Something went wrong.").as_dict(),
    )

    return True


def permission(ctx: Context) -> bool:
    ctx.api.messages.sendMessageEventAnswer(
        event_id=ctx.button.id,
        user_id=ctx.user.id,
        peer_id=ctx.peer.id,
        event_data=ShowSnackbar("⚠️ Lack permission.").as_dict(),
    )

    return True


class ButtonRouter(Router):
    """The router class for BUTTON type events.

    Bounded type:
        EventType.BUTTON
    """

    def __init__(self) -> None:
        self.bounded_type = EventType.BUTTON
        self.handlers["error"] = error
        self.handlers["lack_permission"] = permission

    def route(self, context: Context) -> None:
        """The function extracts the button name from the context
        BUTTON type events, according to which it performs routing
        and initiates certain response actions to call the button handler.

        Args:
            context (Context):  The context of the event.

        Raises:
            RuntimeError: Routing deadlock. The button handler was not found.
        """
        name = context.button.payload.get("name")
        handler = self.handlers.get(name)

        try:
            if handler is None:
                raise NameError(f"Couldn't find a button handler named '{name}'.")

            handler(context)

        except PermissionError as error:
            error_func = self.handlers.get("lack_permission")
            error_func(context)
            logger.info(f"Button handler '{name}' execution canceled: {error}")

        except Exception as error:
            error_func = self.handlers.get("error")
            error_func(context)
            logger.error(f"Error when executing '{name}' button handler: {error}")

    def register(self, name: str = None, check_owner: bool = False) -> None:
        """A decorator that registers a new button handler and assigns it a name.
        Handler functions, marked with this decorator, must have required arguments:
        `ctx`, `payload`

        Args:
            name (str, optional): The name of the button. If not specified,
                            the name of the handler function will be taken.
                            Defaults to None.
            check_owner (bool, oprional): Indicates whether there is a need
                            to check whether the user who pressed the button
                            is the owner of the keyboard under the message.
                            Defaults to True.

        Example:
        ```
            router = Buttons()

            @router.register(name='close')
            def close_button(ctx, payload) -> None:
                pass
        ```
        """

        def decorator(func):
            @wraps(func)
            def wrapper(context: Context):
                # In fact, it's just a shortcut
                payload = context.button.payload

                if check_owner and (context.user.id != payload["owner"]):
                    raise PermissionError(
                        f"User <{context.user.id}> is not keyboard owner."
                    )

                result = func(ctx=context, payload=payload)
                logger.info(f"Event triggered button handler '{name}' execution.")

                return result

            self.handlers[name if name else func.__name__] = wrapper
            return wrapper

        return decorator
