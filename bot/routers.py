from functools import wraps
from typing import Callable, Dict, Tuple, Collection
from collections import namedtuple

from loguru import logger

from .context import Context, EventType

RegistredCollection = Tuple[str, Dict[str, Callable]]


class BaseRouter:
    handlers: Dict[str, Callable] = {}
    bounded_type: EventType = None


class Commands(BaseRouter):
    """The router class for COMMAND type events.

    Bounded type:
        EventType.COMMAND
    """

    def __init__(self) -> None:
        self.bounded_type = EventType.COMMAND

    def route(self, context: Context) -> None:
        """The function extracts the name of the executed command from the context
        of an event of the COMMAND type, according to which it performs routing
        and initiates certain responses actions for calling a command.

        Args:
            context (Context):  The context of the event.

        Raises:
            RuntimeError: Routing deadlock. The command was not found.
        """
        name = context.command.name
        handler = self.handlers.get(name)

        if not handler:
            raise RuntimeError(f"Couldn't find a command named '{name}'.")

        handler(context)

    def register(
        self,
        name: str = None,
        args: Collection[str] = (),
        delete_src: bool = True,
    ) -> None:
        """A decorator that registers a new command and assigns it a name
        and by setting additional parameters. Handler functions, marked
        with this decorator, must have required arguments: ctx, args

        Args:
            name (str, optional): The name of the team. If not specified,
                            the name of the handler function will be taken.
                            Defaults to None.
            args (Collection[str], optional): Positional list of argument names,
                            which the command accepts.
                            Defaults to ().

        Example:
        ```
            router = Commands()

            @router.register(name='test', args=("arg_1", "arg_2"))
            def test_command(ctx, args) -> None:
                pass
        ```
        """

        def decorator(func):
            @wraps(func)
            def wrapper(context: Context):
                """The shell of the function executing the invoked command.
                She is responsible for logging the progress of the command, as well as
                for converting some ctx.command.args object into a NamedTuple instance.

                Args:
                    context (Context): The context of the event.

                Raises:
                    ValueError: The number of arguments is less than stated when declaring the command.

                Returns:
                    Callble: The wrapped executor function.
                """
                pack_arguments = namedtuple("Arguments", args)

                if len(context.command.args) > len(args):
                    packed = pack_arguments(*(context.command.args[0 : len(args)]))
                elif len(context.command.args) == len(args):
                    packed = pack_arguments(*context.command.args)
                else:
                    raise ValueError(
                        f"There are not enough arguments to execute command '{name}'."
                    )

                result = func(ctx=context, args=packed)
                logger.info(
                    f"Event triggered command '{name}' execution with args {packed}."
                )

                if delete_src:
                    context.api.messages.delete(
                        cmids=context.message.cmid,
                        peer_id=context.peer.id,
                        delete_for_all=1,
                    )
                    logger.info(
                        "The message that triggered the command has been deleted."
                    )

                return result

            self.handlers[name if name else func.__name__] = wrapper
            return wrapper

        return decorator


# TODO: write me
class Filters(BaseRouter):
    def __init__(self) -> None:
        self.bounded_type = EventType.MESSAGE


class Buttons(BaseRouter):
    def __init__(self) -> None:
        self.bounded_type = EventType.BUTTON


class Reactions(BaseRouter):
    def __init__(self) -> None:
        self.bounded_type = EventType.REACTION
