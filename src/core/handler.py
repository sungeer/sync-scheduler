import logging

logger = logging.getLogger(__name__)


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    logger.critical(
        'uncaught exception',
        exc_info=(exc_type, exc_value, exc_traceback),
    )
