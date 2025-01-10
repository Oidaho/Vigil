# ./VK-Vigil/main.py

import sys

from loguru import logger

from bot import Bot
from config import configs
from routers import command_router
from db import db_instance
from db.models import (
    Conversation,
    Staff,
    Sanction,
    Menu,
    Queue,
    Filter,
    Delay,
    Word,
    Link,
    Host,
)


def setup_database() -> None:
    db_instance.connect()
    db_instance.create_tables(
        models=[
            Conversation,
            Staff,
            Sanction,
            Menu,
            Queue,
            Filter,
            Delay,
            Word,
            Link,
            Host,
        ]
    )


def setup_logger() -> None:
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
    """Entry point"""
    setup_logger()
    setup_database()

    bot = Bot(
        acces_token=configs.bot.acces_token,
        api_version=configs.bot.api_version,
        group_id=configs.bot.group_id,
    )

    bot.include_router(router=command_router)

    bot.run()


if __name__ == "__main__":
    main()
