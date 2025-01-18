"""The `rules` module provides tools for creating custom routing rules,
applicable both at the router level and at the route (handler function) level.

Classes:
    - `Rule` - A routing rule class.
"""

from abc import ABC, abstractclassmethod

from ..context import Context


class Rule(ABC):
    """A routing rule class. Suitable for defining routing rules
    both at the router level and at the route (handler function) level.
    """

    def __init__(self) -> None:
        pass

    def __call__(self, ctx: Context) -> None:
        if not (rule_check := self.check(ctx)):
            raise RuntimeError(
                f"Rule '{self.__class__.__name__}' was evaluated with the result <{rule_check}>."
            )

    @abstractclassmethod
    def check(self, ctx: Context) -> bool:
        """Checks if the context matches the described rule.

        Args:
            ctx (Context): The message context.

        Returns:
            bool: A boolean value indicating whether the context matches the rule.
        """
