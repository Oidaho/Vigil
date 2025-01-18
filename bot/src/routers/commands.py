"""The `commands` module provides tools for routing events of type COMMAND.

Classes:
    - `CommandRouter`: A router class.
"""

from collections import namedtuple
from functools import wraps
from typing import Collection, List

from loguru import logger

from ..context import Context, EventType
from .base import Router
from .rules import Rule


class CommandRouter(Router):
    """A router class for handling events of type COMMAND.

    Bounded Event Type:
        EventType.COMMAND
    """

    def __init__(self, routing_ruleset: List[Rule] = []) -> None:
        super().__init__(ruleset=routing_ruleset)
        self.bounded_type = EventType.COMMAND

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

        name = context.command.name
        handler = self.handlers.get(name)

        try:
            if handler is None:
                raise NameError(f"Could not find a command named '{name}'")

            return handler(context)

        except (ValueError, RuntimeError) as error:
            logger.warning(f"Command execution canceled: {error}")

        except Exception as error:
            logger.error(f"An error occurred while executing the command: {error}.")

    def register(
        self,
        name: str = None,
        args: Collection[str] = (),
        args_necessary: bool = True,
        delete_src: bool = True,
        execution_ruleset: List[Rule] = [],
    ) -> None:
        """A decorator that registers a new command handler, assigns it a name,
        and configures additional parameters. Handler functions marked with this
        decorator must include the required arguments: `ctx` and `args`.

        Args:
            name (str, optional): The name of the command. If not specified,
                                the name of the handler function will be used.
                                Defaults to None.
            args (Collection[str], optional): A positional list of argument names
                                            that the command accepts.
                                            Defaults to ().
            args_necessary (bool, optional): Specifies whether providing arguments
                                            is mandatory for the command. If False,
                                            the command can be called without arguments.
                                            However, if called with fewer arguments
                                            than required, it will not execute.
                                            Defaults to True.
            delete_src (bool, optional): Enables automatic deletion of the message
                                        that triggered the command.
                                        Defaults to True.
            execution_ruleset (List[Rule], optional): A list of rules that must be validated
                                                    before executing the message handler.

        Example:
            ```python
            router = CommandRouter()

            @router.register(name='test', args=("arg_1", "arg_2"))
            def test_command(ctx, args) -> bool:
                # Response actions here
                return True
            ```
        """

        def decorator(func):
            @wraps(func)
            def wrapper(context: Context):
                for rule in execution_ruleset:
                    rule(context)

                pack_arguments = namedtuple("Arguments", args)

                if len(context.command.args) > len(args):
                    packed = pack_arguments(*(context.command.args[0 : len(args)]))
                elif len(context.command.args) == len(args):
                    packed = pack_arguments(*context.command.args)
                elif len(args) == 0 and not args_necessary:
                    packed = tuple()
                else:
                    raise ValueError(
                        f"Insufficient arguments provided for the command '{name}'."
                    )

                result = func(ctx=context, args=packed)
                logger.info(
                    f"The event triggered the execution of the command '{name}' with arguments: {packed}."
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
