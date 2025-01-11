import json
from typing import Dict, Union

Payload = Dict[str, Union[str, int]]


class ButtonPart:
    def __init__(self, type_: str):
        self.type = type_

    def as_dict(self) -> Payload:
        payload = {key: value for key, value in vars(self).items()}

        return payload

    def json_str(self) -> str:
        return json.dumps(self.as_dict())
