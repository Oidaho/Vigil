from .button_part import ButtonPart, Payload


class Action(ButtonPart):
    payload: Payload = None
    label: str = None


class Callback(Action):
    """Sends a click notification to the server."""

    def __init__(self, label: str, payload: Payload):
        super().__init__("callback")

        self.label = label
        self.payload = payload


class Text(Action):
    """Sends the text of the clicked button to the dialog."""

    def __init__(self, label: str, payload: Payload):
        super().__init__("text")

        self.label = label
        self.payload = payload


class OpenLink(Action):
    """Follows a link."""

    def __init__(self, url: str, label: str, payload: Payload):
        super().__init__("open_link")

        self.link = url
        self.label = label
        self.payload = payload


class Location(Action):
    """Sends geolocation to the dialog."""

    def __init__(self, url: str, label: str, payload: Payload):
        super().__init__("location")

        self.link = url
        self.label = label
        self.payload = payload


class VKPay(Action):
    """Opens the VKPay payment window."""

    def __init__(self, payment_hash: str, label: str, payload: Payload):
        super().__init__("vkpay")

        self.hash = payment_hash
        self.label = label
        self.payload = payload


class OpenApp(Action):
    """Opens the VK Mini App."""

    def __init__(
        self,
        app_hash: str,
        label: str,
        app_id: int,
        owner_id: int,
        payload: Payload,
    ):
        super().__init__("open_app")

        self.hash = app_hash
        self.label = label
        self.payload = payload
        self.app_id = app_id
        self.owner_id = owner_id
