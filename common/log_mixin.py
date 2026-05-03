"""로깅 믹스인."""

from abc import abstractmethod

from loguru import logger


class LogMixin:
    @abstractmethod
    def get_context_info(self) -> str:
        raise NotImplementedError

    def log_info(self, msg: str) -> None:
        logger.info(msg)

    def log_debug(self, msg: str) -> None:
        logger.debug(msg)

    def log_warning(self, msg: str) -> None:
        logger.warning(msg)

    def log_error(self, msg: str) -> None:
        logger.error(msg)
