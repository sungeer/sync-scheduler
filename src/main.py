import os
import signal
import sys
import time

from src.core.logger import setup_logger
from src.core.handler import handle_uncaught_exception
from src.core.http_client import httpx
from src.core.scheduler import build_scheduler
from src.jobs import register_jobs


def on_sigterm(signum, frame):  # noqa
    raise KeyboardInterrupt


def run():
    setup_logger()

    sys.excepthook = handle_uncaught_exception

    signal.signal(signal.SIGTERM, on_sigterm)  # linux
    signal.signal(signal.SIGINT, on_sigterm)  # windows

    httpx.init()

    scheduler = build_scheduler()

    register_jobs(scheduler)

    from loguru import logger

    logger.info('registered %d jobs', len(scheduler.get_jobs()))

    scheduler.start()

    logger.info('scheduler started')

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info('scheduler shutdown')

        httpx.close()

        os._exit(0)
