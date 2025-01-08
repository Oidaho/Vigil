# ./Vigil/bot/bot.py

from concurrent.futures import ThreadPoolExecutor

from loguru import logger
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll

from config import configs

from .context import Context, get_context, EventType
from .routers import BaseRouter


class Bot:
    command_prefix: str = None

    def __init__(self, acces_token: str, api_version: str, group_id: int) -> None:
        self._make_session(acces_token, api_version)
        self._get_longpoll(group_id)
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        logger.info(f"{configs.project_name} ready to work.")

    def _make_session(self, acces_token: str, api_version: str):
        logger.info("Making HTTP session...")
        self.session = VkApi(
            token=acces_token,
            api_version=api_version,
        )

    def _get_longpoll(self, group_id: int):
        logger.info("Creating longpoll instance...")
        self.longpoll = VkBotLongPoll(
            vk=self.session,
            wait=5,
            group_id=group_id,
        )

    @property
    def api(self):
        """Returns the Vkontakte API object for implementation
        retaliatory actions from the bot.

        Returns:
            VkApi: The VKontakte API object.
        """
        return self.session.get_api()

    def set_command_prefix(self, prefix: str) -> None:
        """This function sets the prefix for recognizing the command.
        This means that in case the text of the message event starts
        with a character (or group of characters), the event will be recognized as an attempt
        call the command. In this case, the context of the event will change slightly.

        Args:
            prefix (str): The prefix for recognizing the command.
        """
        self.command_prefix = prefix

    def run(self):
        """Launches the Bot. Starts sending requests to LPS,
        receiving and processing the latest events.
        """
        if self.command_prefix is None:
            self.command_prefix = "/"
            logger.warning(
                f"Command prefix was not set. Bot will use the standard prefix '{self.command_prefix}'."
            )

        logger.info("Starting listening longpoll server.")
        recived_events = self.longpoll.listen

        logger.info("Awaiting events...")
        for event in recived_events():
            if event:
                logger.info("New event recived.")
                logger.debug(event.raw)

                ctx = get_context(event, self.api, self.command_prefix)
                logger.info(f"Context: {ctx}")

                # self.thread_pool.submit(self._handle_event, ctx)
