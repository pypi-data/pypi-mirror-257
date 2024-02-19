"""Logging functions"""

import logging
from typing import Optional


# pylint: disable=locally-disabled, too-few-public-methods
class LogManager:
    """
    Class to create customized logger instances.

    Attributes:
        logger (logging.Logger): Instance of logger configured for LogManager.

    Methods:
        _configure_logger(handlers=None, formatter=None): Private method to configure the logger.
    """

    _shared_log_manager: Optional["LogManager"] = None

    def __init__(self, handlers=None, formatter=None):
        """
        Initializes an instance of Logging with one or more log handlers.

        Args:
            handlers (list, optional): List of log handlers. StreamHandler by default.
            formatter (logging.Formatter, optional): Logger's formatter. None by default.

        Returns:
            None
        """
        self.logger = self._configure_logger(handlers, formatter)

        if not LogManager._shared_log_manager:
            LogManager._shared_log_manager = self

    @classmethod
    def get_instance(cls, handlers=None, formatter=None) -> logging.Logger:
        """_summary_

        Args:
            handlers (list, optional): List of log handlers. StreamHandler by default.
            formatter (logging.Formatter, optional): Logger's formatter. None by default.

        Returns:
            logging.Logger: Configured logger instance.
        """
        if not cls._shared_log_manager:
            cls._shared_log_manager = cls(handlers, formatter)
        return cls._shared_log_manager.logger

    def _configure_logger(self, handlers=None, formatter=None):
        """
        Configures the logger with specified log handlers.

        Args:
            handlers (list, optional): List of log handlers. StreamHandler by default.
            formatter (logging.Formatter, optional): Logger's formatter. None by default.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        formatter = formatter or logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        if handlers is None:
            handlers = [logging.StreamHandler()]  # By default, use a console handler

        for handler in handlers:
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger
