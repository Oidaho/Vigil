from abc import ABC, abstractclassmethod

from ..context import Context


class Rule(ABC):
    def __call__(self, ctx: Context) -> None:
        if not (rule_check := self.check(ctx)):
            raise RuntimeError(
                f"Rule '{self.__class__.__name__}' was checked with the result <{rule_check}>."
            )

    @abstractclassmethod
    def check(self, ctx: Context) -> bool:
        pass
