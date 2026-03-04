import redis
import json
from typing import Optional


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )

    def get(self, key: str) -> Optional[list]:
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: list, expire: int = 300):
        self.client.setex(key, expire, json.dumps(value, default=str))