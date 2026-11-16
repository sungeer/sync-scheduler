import os
import signal
import time

from src.core.logger import setup_logger
from src.core.http_client import httpx
from src.core.scheduler import build_scheduler
from src.jobs import register_jobs


def on_sigterm(signum, frame):  # noqa
    raise KeyboardInterrupt


def run():
    setup_logger()

    signal.signal(signal.SIGTERM, on_sigterm)  # linux
    signal.signal(signal.SIGINT, on_sigterm)  # windows

    httpx.init()

    scheduler = build_scheduler()

    register_jobs(scheduler)

    scheduler.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        httpx.close()

        os._exit(0)
