import logging
from typing import List, Dict
from uuid import uuid4
from datetime import datetime

from .extractor import extract_product
from core.queue_handler import QueueHandler
from core.session_manager import SessionManager, EitaaSession
from core.rate_limiter import RateLimiter


class Crawler:
    def __init__(
        self,
        queue: QueueHandler,
        session_manager: SessionManager,
        rate_limiter: RateLimiter
    ):
        self.queue = queue
        self.session_manager = session_manager
        self.rate_limiter = rate_limiter

    def crawl_channel(self, channel: Dict) -> None:
        "Crawl a single channel and push product jobs to Redis"
        # first choose the session
        session = self.session_manager.get_next_available_session()
        if not session:
            logging.info("No session is available, skipping...")
            return

        # slow down the process
        self.rate_limiter.wait()

        messages = self._fetch_messages(channel, session)

        for message in messages:
            product = extract_product(message)
            if not product:
                continue

            job = self._build_job(channel, message, product)
            self.queue.push(job)

    def _fetch_messages(
            self, channel: Dict, session: EitaaSession) -> List[Dict]:
        "fetch the messages from a single channel"
        # HACK: mock message fetcher; later it must be real Eitaa codes
        # return session.client.get_messages(channel['id'])
        return [
            {"id": "p1", "text": "لپتاپ 30 تومانی", "images": ["img1.jpg"]},
            {"id": "p3", "text": "نامرتبط", "images": []}
        ]

    def _build_job(self, channel: Dict, message: Dict, product: Dict) -> Dict:
        "Build Redis job payload"

        return {
            "job_id": str(uuid4()),
            "source": "eitaa",
            "schema_version": 1.0,

            "channel": {
                "id": channel.get("id"),
                "username": channel.get("username")
            },

            "message": {
                "id": message.get("id"),
                "text": product.get("text", ""),
                "images": product.get("images", [])
            },

            "metadata": {
                "crawled_at": datetime.now().isoformat(),
                "has_price": product.get("has_price")
            }
        }
