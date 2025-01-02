# ./VK-Vigil/bot/bot.py

import time
from concurrent.futures import ThreadPoolExecutor

from loguru import logger
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll

from config import configs

from .context import Context, get_context
from .context import BaseRouter


class Bot:
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

    def _handle_event(self, context: Context) -> None:
        # Placeholder
        time.sleep(3)

        logger.info(f"Event {context.event_id} handled.")

    @property
    def api(self):
        """Returns the Vkontakte API object for implementation
        retaliatory actions from the bot.

        Returns:
            VkApi: The VKontakte API object.
        """
        return self.session.get_api()

    def run(self):
        """Launches the Bot. Starts sending requests to LPS,
        receiving and processing the latest events.
        """
        logger.info("Starting listening longpoll server.")
        recived_events = self.longpoll.listen

        logger.info("Awaiting events...")
        for event in recived_events():
            if event:
                logger.info("New event recived.")
                ctx = get_context(event, self.api)
                logger.info(f"Context: {ctx}")
                logger.debug(event.raw)

                self.thread_pool.submit(self._handle_event, ctx)

    def include(self, router: BaseRouter) -> None:
        # Sketch
        pass
