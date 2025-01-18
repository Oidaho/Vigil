from concurrent.futures import ThreadPoolExecutor

from typing import Dict, Any

from loguru import logger
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll

from config import configs

from .context import Context, get_context, EventType
from .routers.base import Router


class Bot:
    """VK bot class."""

    routing_map: Dict[EventType, Any] = {}

    def __init__(self, acces_token: str, api_version: str, group_id: int) -> None:
        """Initializes the bot.
        Creates a VK session, connects to the LongPoll server (LPS),
        and sets up a thread pool for event processing.

        Args:
            access_token (str): The VK community access token.
            api_version (str): The API version.
            group_id (int): The VK community ID.
        """
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
                if routing_func(ctx):
                    text = "Event handling was completed successfully."
                else:
                    text = "Event handling is completed, however, not all responses could be applied."

                logger.info(text)

            except RuntimeError as error:
                logger.warning(f"Routing canceled: {error}")

            except Exception as error:
                logger.error(
                    f"Something went wrong during the routing of the event: {error}"
                )

    @property
    def api(self):
        """Returns the VKontakte API object to facilitate responsive actions from the bot.

        Returns:
            VkApi: An instance of the VKontakte API object.
        """
        return self.session.get_api()

    def include_router(self, router: Router) -> None:
        """Binds the router to a specific event type, which is defined as its 'bound' type.
        Once the router is bound to a particular event type, all events of that type will be
        processed by the handlers registered within the router.

        Args:
            router (Router): The event router instance.
        """
        self.routing_map[router.bounded_type] = router.route

    def run(self):
        """Initializes and starts the bot. Begins sending requests to the LongPoll server (LPS),
        receives incoming events, and processes them accordingly.
        """
        logger.info("Starting listening longpoll server.")
        recived_events = self.longpoll.listen

        logger.info("Awaiting events...")
        for event in recived_events():
            if event:
                logger.info("New event recived.")
                logger.debug(event.raw)

                ctx = get_context(event, self.api)
                logger.info(f"Context: {ctx}")

                self.thread_pool.submit(self.__handle_ctx, ctx)
