import redis
import json
import logging


class QueueHandler:
    def init(self, host: str, port: int, queue_name: str):
        self.queue_name = queue_name
        self.client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )

    def push(self, job: dict) -> None:
        "Push a single job to Reddis queue"

        try:
            payload = json.dumps(job, ensure_ascii=False)
            self.client.rpush(self.queue_name, payload)
            logging.info("Job pushed to queue: %s", job.get('job_id'))
        except Exception as exc:
            logging.error("Failed to push job to Redis", exc_info=exc)
            raise
