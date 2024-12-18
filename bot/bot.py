# ./VK-Vigil/bot/bot.py

from loguru import logger
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll

from config import configs


class Bot:
    def __init__(self, acces_token: str, api_version: str, group_id: int) -> None:
        self._make_session(acces_token, api_version)
        self._get_longpoll(group_id)
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
        return self.session.get_api()

    def run(self):
        logger.info("Starting listening longpoll server")
        expected_events = self.longpoll.listen

        logger.info("Awaiting events...")
        for raw_event in expected_events():
            if raw_event:
                logger.info("New event recived.")
                logger.debug(f"{raw_event}")
