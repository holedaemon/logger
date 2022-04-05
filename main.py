import asyncio
import os
import sys
import logging

from logger import Logger


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def main():
    token = os.getenv("LOGGER_TOKEN")
    if token is None:
        log.error("$LOGGER_TOKEN is not set")
        sys.exit()

    b = Logger()
    await b.start(token)


if __name__ == "__main__":
    asyncio.run(main())
