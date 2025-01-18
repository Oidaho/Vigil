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
from routers import command_router, button_router
from db import connect_and_prepare, disconnect


def setup_logger() -> None:
    """Configuration of the loguru logger"""
    log_level = "DEBUG" if configs.debug_mode else "INFO"
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

    # db
    connect_and_prepare()

    bot = Bot(
        acces_token=configs.bot.acces_token,
        api_version=configs.bot.api_version,
        group_id=configs.bot.group_id,
    )

    bot.include_router(router=command_router)
    bot.include_router(router=button_router)

    bot.run()

    # db
    disconnect()


if __name__ == "__main__":
    main()
