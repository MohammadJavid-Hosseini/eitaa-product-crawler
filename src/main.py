import logging
import config
from core.queue_handler import QueueHandler
from crawler.crawler import Crawler
from discovery.search import discover_channels


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    queue = QueueHandler(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        queue_name=config.REDIS_QUEUE_NAME
    )

    crawler = Crawler(queue)

    discovered_channels = discover_channels()
    # HACK: for now validation is for granted
    validated_channels = discovered_channels

    for channel in validated_channels:
        crawler.crawl_channel(channel)


if __name__ == "__main__":
    main()
