import uuid
import logging
from datetime import datetime

from core.queue_handler import QueueHandler
import config


def build_fake_job() -> dict:
    "Build a fake product job for testing Redis queue integration"

    return {
        "job_id": str(uuid.uuid4()),
        "source": "eitaa",
        "schema_version": 1.0,

        "channel": {
            "id": "123456",
            "username": "fake_shop_channel"
        },

        "message": {
            "id": "7890",
            "text": "نمونه یک پست فروشگاهی: آیفون17 فقط 200 میلیون",
            "images": [
                "https://example.com/image1.jpg"
            ]
        },

        "metadata": {
            "crawled_at": datetime.now().isoformat(),
            "has_picture": True
        }
    }


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Starting eitaa product crawler MVP")

    queue = QueueHandler(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        queue_name=config.REDIS_QUEUE_NAME
    )

    fake_job = build_fake_job()

    queue.push(job=fake_job)

    logging.info("Finished successfully")


if __name__ == "__main__":
    main()
