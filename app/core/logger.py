from loguru import logger
import sys


logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
)

logger.add(
    "logs/bookingbot.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    encoding="utf-8",
)

__all__ = ["logger"]
