from enum import Enum
from typing import Dict, List

from loguru import logger
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent
from config import configs

Payload = Dict[str, int | str | dict]


class LangType(Enum):
    """The language type of the client from which the event was initiated."""

    RUSSIAN = 0
    UKRAINIAN = 1
    BELARUSIAN_TARASHKIEVICA = 2
    ENGLISH = 3
    SPANISH = 4
    FINNISH = 5
    GERMAN = 6
    ITALIAN = 7
    BULGARIAN = 8
    CROATIAN = 9
    HUNGARIAN = 10
    SERBIAN = 11
    PORTUGUESE = 12
    GREEK = 14
    POLISH = 15
    FRENCH = 16
    KOREAN = 17
    CHINESE = 18
    LITHUANIAN = 19
    JAPANESE = 20
    CZECH = 21
    ESTONIAN = 22
    TATAR = 50
    BASHKIR = 51
    CHUVASH = 52
    SLOVAK = 53
    ROMANIAN = 54
    NORWEGIAN = 55
    LATVIAN = 56
    AZERBAIJANI = 57
    ARMENIAN = 58
    ALBANIAN = 59
    SWEDISH = 60
    DUTCH = 61
    TURKMEN = 62
    GEORGIAN = 63
    DANISH = 64
    UZBEK = 65
    MOLDOVAN = 66
    BURYAT = 67
    THAI = 68
    INDONESIAN = 69
    TAJIK = 70
    SLOVENIAN = 71
    BOSNIAN = 72
    BRAZILIAN_PORTUGUESE = 73
    PERSIAN = 74
    VIETNAMESE = 75
    HINDI = 76
    SINHALA = 77
    BENGALI = 78
    TAGALOG = 79
    MONGOLIAN = 80
    BURMESE = 81
    TURKISH = 82
    NEPALI = 83
    URDU = 85
    KYRGYZ = 87
    PUNJABI = 90
    OSSETIAN = 91
    KANNADA = 94
    SWAHILI = 95
    KAZAKH = 97
    ARABIC = 98
    HEBREW = 99
    PRE_REVOLUTIONARY_RUSSIAN = 100
    ERZYA = 101
    ADYGHEBZE = 102
    YAKUT = 105
    ADYGHE = 106
    UDMURT = 107
    MARI = 108
    BELARUSIAN = 114
    LEZGIAN = 118
    TAIWANESE_HOKKIEN = 119
    KUMYK = 236
    MIRANDESE = 270
    RUSYN = 298
    KARELIAN = 379
    TUVAN = 344
    KALMYK = 357
    TALYSH = 373
    KOMI = 375
    CLASSICAL_UKRAINIAN = 452
    GALICIAN_UKRAINIAN = 454
    KABYLE = 457
    ESPERANTO = 555
    LATIN = 666
    SOVIET_RUSSIAN = 777


class EventType(Enum):
    """The type of the initiated event"""

    MESSAGE = "message_new"
    BUTTON = "message_event"
    REACTION = "message_reaction_event"
    COMMAND = "message_command"


class ContextObject:
    def __init__(self, data: Payload, api: VkApi) -> None:
        """Initializes the class and extracts all necessary data from the payload.

        Args:
            data (Payload): The payload from which data extraction will be attempted.
            api (VkApi): The VK API object.

        Raises:
            AttributeError: An error occurred while extracting an attribute.
        """

    def __repr__(self) -> str:
        """Returns a string representation of the context object.

        Returns:
            str: The string representation.
        """
        return "ContextObject()"


class Peer(ContextObject):
    """A context object providing information about the peer (chat/dialog) where the event occurred."""

    def __init__(self, data: Payload, api: VkApi) -> None:
        if (attempt := data.get("peer_id")) is None:
            if (attempt := data["message"].get("peer_id")) is None:
                raise AttributeError("Error when getting the peer ID")

        self.id: int = attempt
        self.cid: int = self.id - int(2e9)

        self.__api = api

    @property
    def name(self) -> str:
        """Retrieves the peer name."""
        if not hasattr(self, "_Peer__name"):
            peer_info = self.__api.messages.getConversationsById(peer_ids=self.id)
            peer_info = peer_info["items"][0]["chat_settings"]
            self.__name = peer_info.get("title")

        return self.__name

    def __repr__(self) -> str:
        return f"Peer(id={self.id})"


class User(ContextObject):
    """A context object providing information about the user authorized in the VK client."""

    def __init__(self, data: Payload, api: VkApi) -> None:
        if (attempt := data.get("reacted_id")) is None:
            if (attempt := data.get("user_id")) is None:
                if (attempt := data["message"].get("from_id")) is None:
                    raise AttributeError("Error when getting the user ID")

        self.id = attempt
        self.__api = api

    @property
    def full_name(self) -> str:
        """Retrieves the user's full name."""
        if not hasattr(self, "_User__full_name"):
            user_info = self.__api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.__full_name = " ".join(
                [user_info.get("first_name"), user_info.get("last_name")]
            )

        return self.__full_name

    @property
    def first_name(self) -> str:
        """Retrieves the user's first name."""
        if not hasattr(self, "_User__first_name"):
            user_info = self.__api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.__first_name = user_info.get("first_name")

        return self.__first_name

    @property
    def last_name(self) -> str:
        """Retrieves the user's last name."""
        if not hasattr(self, "_User__last_name"):
            user_info = self.__api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.__last_name = user_info.get("last_name")

        return self.__last_name

    @property
    def nick(self) -> str | None:
        """Retrieves the user's last name."""
        if not hasattr(self, "_User__nick"):
            user_info = self.__api.users.get(user_ids=self.id, fields=["domain"])
            user_info = user_info[0]
            self.__nick = user_info.get("domain")

        return self.__nick

    def __repr__(self) -> str:
        return f"User(id={self.id})"


class Reply(ContextObject):
    """A sub-object of the `Message` object, providing information about the message that was replied to or forwarded."""

    def __init__(self, data: Payload, api: VkApi) -> None:
        if (attempt := data.get("conversation_message_id")) is None:
            raise AttributeError("Error when getting the reply message cmID")

        self.id: int = data.get("id")
        self.cmid: int = attempt
        self.text: str = data.get("text")
        self.author: int = data.get("from_id")
        self.peer: int = data.get("peer_id")

        self.__api = api

    def __repr__(self) -> str:
        return f"Reply(id={self.cmid})"


class Command(ContextObject):
    """A context object providing information about the invoked command, if the event is a message and meets certain conditions."""

    def __init__(self, data: Payload, api: VkApi) -> None:
        if (attempt := data["message"].get("text")) is None:
            raise AttributeError("Error when getting the command data")

        self.text: str = attempt

        splited = self.text.split(" ")
        self.name: str = splited[0][1:]
        self.args: List[str] = splited[1:]

        self.__api = api

    def __repr__(self) -> str:
        return f"Command(name={self.name})"


class Message(ContextObject):
    """A context object providing information about the message, if the event is message-related."""

    def __init__(self, data: Payload, api: VkApi) -> None:
        if (attempt := data.get("conversation_message_id")) is None:
            raise AttributeError("Error when getting the message data")

        self.cmid: int = attempt
        self.id: int = data.get("id")
        self.text: str = data.get("text")

        self.__peer_id: int = data.get("peer_id")  # Forced use
        self.__api = api

    @property
    def attachments(self) -> List[str]:
        """Retrieves the message attachments."""
        if not hasattr(self, "_Message__attachments"):
            message_info = self.__api.messages.getByConversationMessageId(
                peer_id=self.__peer_id,
                conversation_message_ids=self.cmid,
            )
            message_info = message_info["items"][0]

            self.__attachments = []
            for attachment in message_info.get("attachments", []):
                self.__attachments.append(attachment.get("type"))

            if message_info.get("geo", False):
                self.__attachments.append("geo")

            if message_info.get("fwd_messages"):
                self.__attachments.append("forward")

            if message_info.get("reply_message"):
                self.__attachments.append("reply")

        return self.__attachments

    @property
    def reply(self) -> Reply | None:
        """Retrieves the message reply."""
        if not hasattr(self, "_Message__reply"):
            message_info = self.__api.messages.getByConversationMessageId(
                peer_id=self.__peer_id,
                conversation_message_ids=self.cmid,
            )
            message_info = message_info["items"][0]

            reply = message_info.get("reply_message")
            logger.debug(f"{reply=}")
            self.__reply = reply if reply is None else Reply(reply, self.__api)

        return self.__reply

    @property
    def forward(self) -> List[Reply]:
        """Retrieves the message forwarded messages."""
        if not hasattr(self, "_Message__forward"):
            message_info = self.__api.messages.getByConversationMessageId(
                peer_id=self.__peer_id,
                conversation_message_ids=self.cmid,
            )
            message_info = message_info["items"][0]

            self.__forward = []
            for reply in message_info.get("fwd_messages"):
                self.__forward.append(Reply(reply, self.__api))

        return self.__forward

    def __repr__(self) -> str:
        return f"Message(cmid={self.cmid})"


class Reaction(ContextObject):
    """A context object providing information about the reaction to a message, if the event is reaction-related."""

    def __init__(self, data: Payload, api: VkApi) -> None:
        self.id: int = data.get("reaction_id", 0)
        self.is_removed: bool = not bool(self.id)

    def __repr__(self) -> str:
        return f"Reaction(id={self.id})"


class Button(ContextObject):
    """A context object providing information about a button press, if the event is button-related."""

    def __init__(self, data: Payload, api: VkApi) -> None:
        if (attempt := data.get("event_id")) is None:
            raise AttributeError("Error when getting the button data")

        self.id: str = attempt
        self.payload: Payload = data.get("payload", {})
        self.cmid: int = data.get("conversation_message_id")

    def __repr__(self) -> str:
        return f"Button(id={self.id})"


class ClientInfo:
    """A context object providing information about the client that initiated the event"""

    def __init__(self, data: Payload, api: VkApi) -> None:
        if (attempt := data.get("client_info")) is None:
            raise AttributeError("Error when getting the client info.")

        self.lang: LangType = LangType(attempt.get("lang_id"))
        self.inline_keyboard: bool = attempt.get("inline_keyboard")
        self.keyboard: bool = attempt.get("keyboard")
        self.avalibleactions: List[str] = attempt.get("button_actions")

    def __repr__(self) -> str:
        return f"ClientInfo(lang={self.lang.name})"


class Context:
    """The context of the initiated event"""

    __attribute_class = {
        "client": ClientInfo,
        "peer": Peer,
        "user": User,
        "reaction": Reaction,
        "message": Message,
        "button": Button,
        "command": Command,
    }

    def __init__(self, raw: Payload, api: VkApi) -> None:
        """Takes a raw VK event as a payload, determines the event type,
        and attempts to parse the necessary attributes (context objects) accordingly.

        Args:
            raw (Payload): The raw VK event in the form of a payload.
            api (VkApi): The VK API object.
        """
        self.api = api

        self.event_type: EventType = EventType(raw["type"])
        self.event_id: str = raw["event_id"]
        self.group_id: int = raw["group_id"]

        event_object = raw["object"]

        self.__extract_attribute("peer", event_object)
        self.__extract_attribute("user", event_object)

        if self.event_type == EventType.MESSAGE:
            self.__extract_attribute("client", event_object)
            self.__extract_attribute("message", event_object)

            if self.message.text.startswith(configs.bot.command_prefix):
                self.event_type = EventType("message_command")
                self.__extract_attribute("command", event_object)

        elif self.event_type == EventType.BUTTON:
            self.__extract_attribute("button", event_object)

        elif self.event_type == EventType.REACTION:
            self.__extract_attribute("reaction", event_object)

    def __extract_attribute(self, attr_name: str, event_object: Payload) -> None:
        value = event_object.get(attr_name, event_object)
        setattr(self, attr_name, self.__attribute_class[attr_name](value, self.api))
        logger.debug(f"Attribute '{attr_name}' extracted: {getattr(self, attr_name)}.")

    def __repr__(self) -> str:
        return f"EventContext(id={self.event_id}, type={self.event_type.name}, group={self.group_id})"


def get_context(event: VkBotEvent, api: VkApi) -> Context:
    """Extracts all required information from the VK event and,
    if necessary, performs additional requests to the VK API to
    retrieve supplementary data.

    Args:
        event (VkBotEvent): The VK event object.
        api (VkApi): An instance of the VkApi class for interacting with the VK API.
        command_prefix (str): The prefix used by the bot to identify commands.

    Returns:
        Context: An object representing the event context.
    """
    try:
        ctx = Context(event.raw, api)

    except ValueError as error:
        logger.warning(
            "Unable to load event context. Received an event with an unknown type."
        )
        logger.debug(f"Error details: {error}")

    except AttributeError as error:
        logger.error(
            f"An error occurred while retrieving the message context: {error}."
        )

    else:
        return ctx
