import logging
import config
import argparse
from core.queue_handler import QueueHandler
from core.session_manager import SessionManager
from core.rate_limiter import RateLimiter
from core.ai_service import CoreAIService
from discovery.search import discover_channels
from discovery.keyword_gen import KeywordGenerator
from validation.channel_validator import ChannelValidator
from crawler.crawler import Crawler


def parse_args():
    parser = argparse.ArgumentParser(description="Eitaa Product Crawler")
    parser.add_argument(
        "--category",
        type=str,
        default="کالا و محصولات فروشی",
        help="Product category for discovery (default: کالا و محصولات فروشی)"
    )
    return parser.parse_args()


def main():
    # logging settings
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Started Eitaa product crawler (MVP)")

    # parsing the user args
    args = parse_args()

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

    # instanciate AI worker
    ai_service = CoreAIService()
    keyword_gen = KeywordGenerator(ai_service)

    # instanciate validator
    validator = ChannelValidator(ai_service)

    discovered_channels = discover_channels(
        category=args.category,
        keyword_gen=keyword_gen
    )
    logging.info(f"Search for category: {args.category}")
    logging.info("Discovered %s channels", len(discovered_channels))

    validated_channels = [
        ch for ch in discovered_channels if validator.validate(ch)
    ]
    logging.info("Validated %s channels", len(validated_channels))

    crawler = Crawler(queue, session_manager, rate_limiter)

    for channel in validated_channels:
        crawler.crawl_channel(channel)

    logging.info("Finished Successfully")


if __name__ == "__main__":
    main()
