import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.propagate = True


class InternalLogger:
    @staticmethod
    def LogInfo(msg: str):
        logger.info(msg)

    @staticmethod
    def LogDebug(msg: str):
        logger.debug(msg)

    @staticmethod
    def LogError(msg: str):
        logger.error(msg)