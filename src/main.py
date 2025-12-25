import logging
import config
from core.queue_handler import QueueHandler
from core.session_manager import SessionManager
from core.rate_limiter import RateLimiter
from core.ai_service import CoreAIService
from discovery.search import discover_channels
from discovery.keyword_gen import KeywordGenerator
from validation.channel_validator import validate_channels
from crawler.crawler import Crawler


def main():
    # logging settings
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Started Eitaa product crawler (MVP)")

    # make the queue
    queue = QueueHandler(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        queue_name=config.REDIS_QUEUE_NAME
    )
    logging.info("the pfoduct_jobs queue is created")

    # initialize the session-manager and the rate-limiter
    session_manager = SessionManager()
    rate_limiter = RateLimiter()
    session_manager.add_session("1234ioq", "ali_test")

    ai_service = CoreAIService()
    keyword_gen = KeywordGenerator(ai_service)

    # FIX: later the category comes from user or settings
    discovered_channels = discover_channels(
        category='پوشاک مردانه', keyword_gen=keyword_gen)
    logging.info("Discovered %s channels", len(discovered_channels))

    validated_channels = validate_channels(discovered_channels)
    logging.info("Validated %s channels", len(validated_channels))

    crawler = Crawler(queue, session_manager, rate_limiter)

    for channel in validated_channels:
        crawler.crawl_channel(channel)

    logging.info("Finished Successfully")


if __name__ == "__main__":
    main()
