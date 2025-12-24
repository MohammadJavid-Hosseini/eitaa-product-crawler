import logging
import config
from core.queue_handler import QueueHandler
from core.session_manager import SessionManager
from core.rate_limiter import RateLimiter
from crawler.crawler import Crawler
from discovery.search import discover_channels
from validation.channel_validator import validate_channels


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Started Eitaa product crawler (MVP)")

    queue = QueueHandler(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        queue_name=config.REDIS_QUEUE_NAME
    )
    logging.info("the pfoduct_jobs queue is created")

    discovered_channels = discover_channels()
    logging.info("Discovered %s channels", len(discovered_channels))

    validated_channels = validate_channels(discovered_channels)
    logging.info("Validated %s channels", len(validated_channels))

    session_manager = SessionManager()
    rate_limiter = RateLimiter()
    session_manager.add_session("1234ioq", "ali_test")
    crawler = Crawler(queue, session_manager, rate_limiter)

    for channel in validated_channels:
        crawler.crawl_channel(channel)

    logging.info("Finished Successfully")


if __name__ == "__main__":
    main()
