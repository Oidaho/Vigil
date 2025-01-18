import json
from enum import Enum
from typing import Any

from .actions import Action
from .button_part import Payload


class ButtonColor(Enum):
    """Available colors for keyboard buttons."""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class Button:
    """A button, which is part of a VK keyboard layout."""

    def __init__(self, action: Action, color: ButtonColor, owner_id: int):
        self.action = action
        self.color = color
        self.owner_id = owner_id

    def as_dict(self) -> Payload:
        """Returns a dictionary representation of the data in the class.

        Returns:
            Payload: A dictionary representation, the payload.
        """
        self.action.payload.update({"owner": self.owner_id})

        data = {"action": self.action.as_dict(), "color": self.color.value}

        return data


class Keyboard:
    """A class representing a VK keyboard. Uses a builder interface for initialization
    and can be converted into a JSON string.
    """

    def __init__(self, inline: bool, one_time: bool, owner_id: int):
        self.buttons_total: int = 0
        self.owner_id = owner_id
        self.inline: bool = inline
        self.one_time: bool = one_time
        self.rows: list = []

    def add_row(self) -> Any:
        """Adds a new row to the list of buttons. Each row represents a set of buttons.

        Raises:
            ValueError: The maximum number of rows in the keyboard has been reached.
            RuntimeError: The previous row in the keyboard is empty.

        Returns:
            Any: An instance of the same class.
        """
        if len(self.rows) >= 5:
            raise ValueError("The maximum count of rows has been exceeded.")

        if self.rows and not self.rows[-1]:
            raise RuntimeError("Can not create new row while previous is empty.")

        self.rows.append([])

        return self

    def add_button(self, name: str, action: Action, color: ButtonColor) -> Any:
        """Adds a new button to the keyboard, selecting the last created row for insertion.

        Args:
            name (str): The technical name of the button.
            action (Action): The action performed when the button is pressed.
            color (ButtonColor): The color of the button.

        Raises:
            RuntimeError: No rows have been added to the keyboard.
            ValueError: The maximum number of buttons in the keyboard has been reached.
            ValueError: The maximum number of buttons in a row has been reached.

        Returns:
            Any: An instance of the same class.
        """
        if not self.rows:
            raise RuntimeError("No rows have been added to the keyboard.")

        if (self.inline and self.buttons_total >= 10) or (
            not self.inline and self.buttons_total >= 40
        ):
            raise ValueError(
                "The maximum number of buttons in the keyboard has been reached."
            )

        if (self.inline and len(self.rows[-1]) >= 6) or (
            not self.inline and len(self.rows[-1]) >= 10
        ):
            raise ValueError("The maximum number of buttons in a row has been reached.")

        action.payload.update({"name": name})

        new_button = Button(action, color, self.owner_id).as_dict()
        self.rows[-1].append(new_button)
        self.buttons_total += 1

        return self

    def as_dict(self) -> Payload:
        """Returns a dictionary representation of the data in the class.

        Returns:
            Payload: A dictionary representation, the payload.
        """
        body = {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": self.rows,
        }

        return body

    def json_str(self) -> str:
        """Returns a JSON string representation of the data in the class.

        Returns:
            str: A JSON string.
        """
        return json.dumps(self.as_dict())


class EmptyKeyboard(Keyboard):
    """A class representing an empty keyboard, used to remove the keyboard from a message."""

    def __init__(self) -> None:
        return

    def as_dict(self) -> Payload:
        return {}
