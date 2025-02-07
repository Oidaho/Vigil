"""Startup script for the 'bot' container.

Performs the following actions:
    - Configures the logger using the `loguru` module.
    - Establishes a connection to the database.
    - Initializes the bot and starts its operation.
"""

import sys

from loguru import logger

from src import Bot
from config import configs
from routers import command_router, button_router, message_router
import db


def setup_logger() -> None:
    """Configuration of the loguru logger"""
    log_level = "DEBUG" if configs.DEBUG_MODE else "INFO"
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format=" | ".join(
            (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green>",
                "<red>{module}</red>",
                "<level>{level}</level>",
                "{message}",
            )
        ),
        level=log_level,
    )


def main() -> None:
    """Program entry point"""
    setup_logger()

    db.connect_and_prepare()

    bot = Bot(
        acces_token=configs.bot.GROUP_TOKEN,
        api_version=configs.bot.API_VERSION,
        group_id=configs.bot.GROUP_ID,
    )

    bot.include_router(router=command_router)
    bot.include_router(router=button_router)
    bot.include_router(router=message_router)
    bot.run()

    db.disconnect()


if __name__ == "__main__":
    main()
