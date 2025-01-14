import json
from enum import Enum
from typing import Any

from .actions import Action
from .button_part import Payload


class ButtonColor(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class Button:
    def __init__(self, action: Action, color: ButtonColor, owner_id: int):
        self.action = action
        self.color = color
        self.owner_id = owner_id

    def as_dict(self) -> Payload:
        self.action.payload.update({"owner": self.owner_id})

        data = {"action": self.action.as_dict(), "color": self.color.value}

        return data


class Keyboard:
    def __init__(self, inline: bool, one_time: bool, owner_id: int):
        self.owner_id = owner_id
        self.inline: bool = inline
        self.one_time: bool = one_time
        self.rows: list = []

    def add_row(self) -> Any:
        if len(self.rows) > 6:
            raise ValueError("The maximum count of rows has been exceeded.")

        if self.rows and not self.rows[-1]:
            raise RuntimeError("Can not create new row while previous is empty.")

        self.rows.append([])

        return self

    def add_button(self, name: str, action: Action, color: ButtonColor) -> Any:
        # TODO: Добавить ограничение по кнопкам в строке
        if not self.rows:
            raise RuntimeError("Missing rows.")

        action.payload.update({"name": name})

        new_button = Button(action, color, self.owner_id).as_dict()
        self.rows[-1].append(new_button)

        return self

    def as_dict(self) -> Payload:
        body = {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": self.rows,
        }

        return body

    def json_str(self) -> str:
        return json.dumps(self.as_dict())


class EmptyKeyboard(Keyboard):
    def __init__(self) -> None:
        return

    def as_dict(self) -> Payload:
        return {}
