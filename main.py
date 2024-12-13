# ./VK-Vigil/main.py

import sys
from loguru import logger


def setup_logger() -> None:
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
        level="DEBUG",
    )


def main():
    """Program entry point."""

    setup_logger()


if __name__ == "__main__":
    main()
