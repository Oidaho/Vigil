from enum import Enum
from typing import Dict, List

from loguru import logger
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent

Payload = Dict[str, int | str | dict]


class LangType(Enum):
    RUSSIAN = 0


class EventType(Enum):
    MESSAGE = "message_new"
    BUTTON = "message_event"
    REACTION = "message_reaction_event"


class Message:
    pass


class Reaction:
    pass


class Button:
    pass


class ClientInfo:
    def __init__(self, data: Payload, api: VkApi) -> None:
        if attempt := data.get("client_info") is None:
            raise ValueError("Error when getting the client info.")

        self.lang: LangType = LangType(attempt.get("lang_id"))
        self.inline_keyboard: bool = attempt.get("inline_keyboard")
        self.keyboard: bool = attempt.get("keyboard")
        self.avalibleactions: List[str] = attempt.get("button_actions")

    def __repr__(self) -> str:
        return f"ClientInfo(lang={self.lang})"


class Peer:
    def __init__(self, data: Payload, api: VkApi) -> None:
        if attempt := data.get("peer_id") is None:
            if attempt := data["message"].get("peer_id") is None:
                raise ValueError("Error when getting the peer ID.")

        self.id: int = attempt
        self.cid: int = self.id - int(2e9)
        self.api = api

    @property
    def name(self) -> str:
        if not hasattr(self, "full_name"):
            peer_info = self.api.messages.getConversationsById(peer_ids=self.id)
            peer_info = peer_info["items"][0]["chat_settings"]
            self.name = peer_info.get("title")

        return self.name

    def __repr__(self) -> str:
        return f"Peer({self.id})"


class User:
    def __init__(self, data: Payload, api: VkApi) -> None:
        if attempt := data.get("reacted_id") is None:
            if attempt := data.get("user_id") is None:
                if attempt := data["message"].get("from_id") is None:
                    raise ValueError("Error when getting the user ID.")

        self.id = attempt
        self.api = api

    @property
    def full_name(self) -> str:
        if not hasattr(self, "full_name"):
            user_info = self._api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.full_name = " ".join(
                [user_info.get("first_name"), user_info.get("last_name")]
            )

        return self.full_name

    @property
    def first_name(self) -> str:
        if not hasattr(self, "first_name"):
            user_info = self.api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.first_name = user_info.get("first_name")

        return self.first_name

    @property
    def last_name(self) -> str:
        if not hasattr(self, "last_name"):
            user_info = self.api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.last_name = user_info.get("last_name")

        return self.last_name

    @property
    def nick(self) -> str:
        if not hasattr(self, "nick"):
            user_info = self.api.users.get(user_ids=self.id, fields=["domain"])
            user_info = user_info[0]
            self.nick = user_info.get("domain")

        return self.nick

    def __repr__(self) -> str:
        return f"User({self.id})"


class Context:
    __attribute_info = {
        "client_info": {"key": "client_info", "class": ClientInfo},
        "peer": {"key": "peer", "class": Peer},
        "user": {"key": "user", "class": User},
        "message": {"key": "message", "class": Message},
        "payload": {"key": "payload", "class": Payload},
        "reaction": {"key": "reaction_id", "class": Reaction},
    }

    def __init__(self, raw: Payload, api: VkApi) -> None:
        self.api = api

        self.event_type: EventType = EventType(raw["type"])
        self.event_id: str = raw["event_id"]
        self.group_id: int = raw["group_id"]

        self.__extract_attribute("peer", raw["object"])
        self.__extract_attribute("user", raw["object"])

        if self.event_type == EventType.MESSAGE:
            self.__extract_attribute("client_info", raw["object"])
            self.__extract_attribute("message", raw["object"])

        elif self.event_type == EventType.BUTTON:
            self.__extract_attribute("payload", raw["object"])

        elif self.event_type == EventType.REACTION:
            self.__extract_attribute("reaction", raw["object"])

        self.__delete_unused()

    def __extract_attribute(self, attr_name: str, event_object: Payload) -> None:
        value = event_object.pop(attr_name, default=event_object)
        attr = self.__attribute_info[attr_name]["key"]
        setattr(self, attr, self.__attribute_info[attr_name]["class"](value, self.api))

    def __delete_unused(self) -> None:
        delattr(self, "__attribute_info")
        delattr(self, "api")

    def __repr__(self) -> str:
        return f"EventContext(id={self.event_id}, type={self.event_type}, group={self.group_id})"


def get_context(self, event: VkBotEvent, api: VkApi) -> Context:
    try:
        ctx = Context(event.raw, api)

    except ValueError:
        logger.warning("Unable to load event context. Recived event with unknown type.")

    except Exception as error:
        logger.error(
            f"Something went wrong while receiving the message context: {error}"
        )

    else:
        return ctx
