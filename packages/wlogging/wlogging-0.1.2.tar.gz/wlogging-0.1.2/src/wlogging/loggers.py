"""
"""


#[
from __future__ import annotations

import types

import logging
from . import formatters as _formatters
#]


__all__ = [
    "get_colored_logger",
]


def get_colored_logger(
    name: str | None = None,
    propagate: bool = True,
    level: int = logging.WARNING,
    format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    remove_existing_handlers: bool = True,
) -> logging.Logger:
    """
    """
    logger = logging.getLogger(name, )
    logger.clear_handlers = types.MethodType(_clear_handlers, logger, )
    logger.propagate = propagate
    if remove_existing_handlers:
        logger.clear_handlers()
    handler = logging.StreamHandler()
    formatter = _formatters.ColoredFormatter(format, )
    handler.set_formatter(formatter, )
    logger.addHandler(handler, )
    logger.setLevel(level, )
    logger._decorated = True
    return logger


def _clear_handlers(logger: Logger, ) -> None:
    for handler in logger.handlers:
        logger.remove_handler(handler, )


