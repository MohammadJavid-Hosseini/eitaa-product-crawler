from typing import List, Dict
from uuid import uuid4
from datetime import datetime

from .extractor import extract_product
from core.queue_handler import QueueHandler


class Crawler:
    def __init__(self, queue: QueueHandler):
        self.queue = queue

    def crawl_channel(self, channel: Dict) -> None:
        "Crawl a single channel and push product jobs to Redis"
        messages = self._fetch_messages(channel)

        for message in messages:
            product = extract_product(message)
            if not product:
                continue

            job = self._build_job(channel, message, product)
            self.queue.push(job)

    def _fetch_messages(self, channel: Dict) -> List[Dict]:
        "fetch the messages from a single channel"
        # HACK: mock message fetcher; later it must be dynamic
        return [
            {
                "id": "p1",
                "text": "فروش به صرفه ترین لپتاپ نسل 13: فقط 30 میلیون تومان",
                "images": ["https://example2.com/image_laptop.jpg"]
            },
            {
                "id": "p3",
                "text": "نباید بره",
                "images": []
            }
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
