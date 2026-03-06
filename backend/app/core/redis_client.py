import json
import logging
import os
from typing import Optional

import redis
from redis.exceptions import RedisError


logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL")
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.enabled = True

        if redis_url:
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
        else:
            self.client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
            )

        try:
            self.client.ping()
            logger.info("Redis cache enabled.")
        except RedisError as exc:
            self.enabled = False
            logger.warning("Redis unavailable. Continuing without cache. Error: %s", exc)

    def get(self, key: str) -> Optional[list]:
        if not self.enabled:
            return None

        try:
            data = self.client.get(key)
        except RedisError as exc:
            self.enabled = False
            logger.warning("Redis GET failed. Disabling cache. Error: %s", exc)
            return None

        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: list, expire: int = 300):
        if not self.enabled:
            return

        try:
            self.client.setex(key, expire, json.dumps(value, default=str))
        except RedisError as exc:
            self.enabled = False
            logger.warning("Redis SET failed. Disabling cache. Error: %s", exc)
