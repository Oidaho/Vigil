import json
from typing import Dict, Union

Payload = Dict[str, Union[str, int]]


class ButtonComponent:
    """Base class for a button component."""

    def __init__(self, type_: str):
        self.type = type_

    def as_dict(self) -> Payload:
        """Returns a dictionary representation of the data in the class.

        Returns:
            Payload: A dictionary representation, the payload.
        """
        payload = {key: value for key, value in vars(self).items()}

        return payload

    def json_str(self) -> str:
        """Returns a JSON string representation of the data in the class.

        Returns:
            str: A JSON string.
        """
        return json.dumps(self.as_dict())
