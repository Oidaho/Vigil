from .button_part import ButtonPart


class Answer(ButtonPart):
    pass


class ShowSnackbar(Answer):
    """Answers to button pressing by calling snackbar."""

    def __init__(self, text: str):
        super().__init__("show_snackbar")

        self.text = text


class OpenLink(Answer):
    """Answers to button pressing by redirecting to the link."""

    def __init__(self, url: str):
        super().__init__("open_link")

        self.link = url


class OpenApp(Answer):
    """Answers to button pressing by opening a mini-app."""

    def __init__(self, app_hash: str, app_id: int, owner_id: int):
        super().__init__("open_app")

        self.hash = app_hash
        self.app_id = app_id
        self.owner_id = owner_id
