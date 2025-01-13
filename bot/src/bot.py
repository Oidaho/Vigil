# ./Vigil/bot/bot.py

from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

from loguru import logger
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll

from config import configs

from .context import Context, get_context, EventType
from .routers.base import Router


STD_COMMAND_PREFIX = "/"


class Bot:
    command_prefix: str = None
    routing_map: Dict[EventType, Any] = {}

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

    def __handle_ctx(self, ctx: Context) -> None:
        routing_func = self.routing_map.get(ctx.event_type, None)

        if routing_func is None:
            logger.warning(
                f"Skipping event <{ctx.event_id}| {ctx.event_type}>. There is no suitable router."
            )

        else:
            try:
                routing_func(ctx)

            except RuntimeError as error:
                logger.warning(f"Routing canceled: {error}")

            except Exception as error:
                logger.error(
                    f"Something went wrong during the routing of the event: {error}"
                )

    @property
    def api(self):
        """Returns the Vkontakte API object for implementation
        retaliatory actions from the bot.

        Returns:
            VkApi: The VKontakte API object.
        """
        return self.session.get_api()

    def include_router(self, router: Router) -> None:
        """Binds the router to a specific type of event,
        which is specified for it as 'bounded'. In case of binding
        router to a certain type of event - these events will start
        processed by handlers registered in the router.

        Args:
            router (Router): Event router.
        """
        self.routing_map[router.bounded_type] = router.route

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
            self.command_prefix = STD_COMMAND_PREFIX
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

                self.thread_pool.submit(self.__handle_ctx, ctx)
