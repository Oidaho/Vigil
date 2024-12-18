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


class Peer:
    def __init__(self, data: Payload, api: VkApi) -> None:
        if attempt := data.get("peer_id") is None:
            if attempt := data["message"].get("peer_id") is None:
                raise ValueError("Error when getting the peer ID.")

        self.id: int = attempt
        self.cid: int = self.id - int(2e9)
        self.__api = api

    @property
    def name(self) -> str:
        if not hasattr(self, "__name"):
            peer_info = self.__api.messages.getConversationsById(peer_ids=self.id)
            peer_info = peer_info["items"][0]["chat_settings"]
            self.__name = peer_info.get("title")

        return self.__name

    def __repr__(self) -> str:
        return f"Peer({self.id})"


class User:
    def __init__(self, data: Payload, api: VkApi) -> None:
        if attempt := data.get("reacted_id") is None:
            if attempt := data.get("user_id") is None:
                if attempt := data["message"].get("from_id") is None:
                    raise ValueError("Error when getting the user ID.")

        self.id = attempt
        self.__api = api

    @property
    def full_name(self) -> str:
        if not hasattr(self, "__full_name"):
            user_info = self.__api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.__full_name = " ".join(
                [user_info.get("first_name"), user_info.get("last_name")]
            )

        return self.__full_name

    @property
    def first_name(self) -> str:
        if not hasattr(self, "__first_name"):
            user_info = self.__api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.__first_name = user_info.get("first_name")

        return self.__first_name

    @property
    def last_name(self) -> str:
        if not hasattr(self, "__last_name"):
            user_info = self.__api.users.get(user_ids=self.id)
            user_info = user_info[0]
            self.__last_name = user_info.get("last_name")

        return self.__last_name

    @property
    def nick(self) -> str | None:
        if not hasattr(self, "__nick"):
            user_info = self.__api.users.get(user_ids=self.id, fields=["domain"])
            user_info = user_info[0]
            self.__nick = user_info.get("domain")

        return self.__nick

    def __repr__(self) -> str:
        return f"User({self.id})"


# At the moment, we are not interested in having nested reply and fwd inside Reply.
# As is peer_id accounting. If the message is a reply - peer, the id matches the parent message.
# And we are not interested in fwd messages. There's nothing to do with them.
class Reply:
    def __init__(self, data: Payload, api: VkApi) -> None:
        if attempt := data.get("conversation_message_id") is None:
            raise ValueError("Error when getting the reply message cmID.")

        self.cmid: int = attempt
        self.__peer_id: int = data.get("peer_id")  # Forced use
        self.__api = api

    @property
    def text(self) -> str:
        if not hasattr(self, "__text"):
            message_info = self.__api.messages.getByConversationMessageId(
                peer_id=self.__peer_id,
                conversation_message_ids=self.cmid,
            )
            message_info = message_info["items"][0]
            self.__text = message_info.get("text")

        return self.__text


class Message:
    def __init__(self, data: Payload, api: VkApi) -> None:
        if attempt := data.get("message") is None:
            raise ValueError("Error when getting the message data.")

        self.id: int = attempt.get("id")
        self.cmid: int = attempt.get("conversation_message_id")
        self.__peer_id: int = attempt.get("peer_id")  # Forced use
        self.__api = api

    @property
    def text(self) -> str:
        if not hasattr(self, "__text"):
            message_info = self.__api.messages.getByConversationMessageId(
                peer_id=self.__peer_id,
                conversation_message_ids=self.cmid,
            )
            message_info = message_info["items"][0]
            self.__text = message_info.get("text")

        return self.__text

    @property
    def attachments(self) -> List[str]:
        if not hasattr(self, "__attachments"):
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

        return self.__attachments

    @property
    def reply(self) -> Reply | None:
        if not hasattr(self, "__reply"):
            message_info = self.__api.messages.getByConversationMessageId(
                peer_id=self.__peer_id,
                conversation_message_ids=self.cmid,
            )
            message_info = message_info["items"][0]

            reply = message_info.get("reply_message")
            self.__reply = reply if reply is None else Reply(reply, self.__api)

        return self.__reply

    @property
    def forward(self) -> List[Reply]:
        if not hasattr(self, "__forward"):
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
        return f"Message(cmid={self.cmdid})"


class Reaction:
    def __init__(self, data: Payload, api: VkApi) -> None:
        self.id: int = data.get("reaction_id", 0)
        self.is_removed: bool = not bool(self.id)

    def __repr__(self) -> str:
        return f"Reaction(id={self.id})"


class Button:
    def __init__(self, data: Payload, api: VkApi) -> None:
        if attempt := data.get("event_id") is None:
            raise ValueError("Error when getting the button data.")

        self.id: str = attempt
        self.payload: Payload = data.get("payload", {})

    def __repr__(self) -> str:
        return f"Button(id={self.id})"


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


class Context:
    __attribute_class = {
        "client_info": ClientInfo,
        "peer": Peer,
        "user": User,
        "reaction": Reaction,
        "message": Message,
        "payload": Payload,
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

        delattr(self, "__attribute_class")

    def __extract_attribute(self, attr_name: str, event_object: Payload) -> None:
        value = event_object.pop(attr_name, default=event_object)
        setattr(self, attr_name, self.__attribute_class[attr_name](value, self.api))

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
