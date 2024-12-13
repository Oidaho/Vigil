# ./VK-Vigil/main.py

import sys

from loguru import logger

from bot import Bot
from config import configs


def setup_logger() -> None:
    log_level = "DEBUG" if configs.debug_mode else "INFO"
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format=" | ".join(
            (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
                "<red>{module}</red>"
                "<level>{level}</level>"
                "{message}"
            )
        ),
        level=log_level,
    )


def main() -> None:
    """Program entry point."""
    setup_logger()

    vigil = Bot(
        acces_token=configs.bot.acces_token,
        api_version=configs.bot.api_version,
    )
    vigil.run()


if __name__ == "__main__":
    main()
