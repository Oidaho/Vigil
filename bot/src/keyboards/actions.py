from typing import Optional

from .button_part import ButtonComponent, Payload


class Action(ButtonComponent):
    payload: Payload = None
    label: str = None


class Callback(Action):
    """Sends a click notification to the server upon button press."""

    def __init__(self, label: str, payload: Optional[Payload] = None):
        super().__init__("callback")

        self.label = label
        self.payload = payload or dict()


class Text(Action):
    """Sends the text associated with the clicked button to the dialog."""

    def __init__(self, label: str, payload: Optional[Payload] = None):
        super().__init__("text")

        self.label = label
        self.payload = payload or dict()


class OpenLink(Action):
    """Navigates to a specified link."""

    def __init__(self, url: str, label: str, payload: Optional[Payload] = None):
        super().__init__("open_link")

        self.link = url
        self.label = label
        self.payload = payload or dict()


class Location(Action):
    """Sends the current geolocation to the dialog."""

    def __init__(self, url: str, label: str, payload: Optional[Payload] = None):
        super().__init__("location")

        self.link = url
        self.label = label
        self.payload = payload or dict()


class VKPay(Action):
    """Opens the VKPay payment window for transactions."""

    def __init__(
        self, payment_hash: str, label: str, payload: Optional[Payload] = None
    ):
        super().__init__("vkpay")

        self.hash = payment_hash
        self.label = label
        self.payload = payload or dict()


class OpenApp(Action):
    """Launches the VK Mini App."""

    def __init__(
        self,
        app_hash: str,
        label: str,
        app_id: int,
        owner_id: int,
        payload: Optional[Payload] = None,
    ):
        super().__init__("open_app")

        self.hash = app_hash
        self.label = label
        self.app_id = app_id
        self.owner_id = owner_id
        self.payload = payload or dict()
