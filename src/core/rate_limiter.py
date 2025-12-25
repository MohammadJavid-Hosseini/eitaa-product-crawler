import time
import random
import logging


class RateLimiter:
    def __init__(self, requests_per_minute: int = 20):
        # requests_per_minute: How many requests allowed in 60 seconds.
        self.interval = 60.0 / requests_per_minute
        self.last_request_time = 0

    def wait(self):
        """Standard synchronous wait"""
        unused_time = time.time() - self.last_request_time

        # Calculate how much we need to wait
        wait_time = self.interval - unused_time

        if wait_time > 0:
            # Add 10-20% random jitter to look human
            jitter = wait_time * random.uniform(0.1, 0.2)
            total_sleep = wait_time + jitter

            logging.debug(f"RateLimiter: Sleeping for {total_sleep:.2f}s")
            time.sleep(total_sleep)

        self.last_request_time = time.time()
