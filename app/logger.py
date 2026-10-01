import logging
import sys

from app.config import LOG_LEVEL

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)-7s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

logging.getLogger("app").setLevel(LOG_LEVEL)


def get_logger(name):
    return logging.getLogger(name)
