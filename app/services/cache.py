import redis
import json
from typing import Optional, Any

class Cache:
    def __init__(self, host='localhost', port=6379, db=0, password: Optional[str] = None):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True  # Automatically decode responses from bytes to strings
        )

    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except redis.RedisError as e:
            # Handle or log Redis errors
            print(f"Error getting key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> None:
        try:
            value = json.dumps(value)
            self.client.set(key, value, ex=ex)  # Optional TTL
        except redis.RedisError as e:
            # Handle or log Redis errors
            print(f"Error setting key {key}: {e}")

    def exists(self, key: str) -> bool:
        try:
            return self.client.exists(key) > 0
        except redis.RedisError as e:
            # Handle or log Redis errors
            print(f"Error checking existence of key {key}: {e}")
            return False
    
    def update(self, key: str, value: Any) -> bool:
        if self.exists(key):
            try:
                value = json.dumps(value)
                self.set(key, value)
                return True
            except redis.RedisError as e:
                # Handle or log Redis errors
                print(f"Error updating key {key}: {e}")
        return False

    def delete(self, key: str) -> bool:
        if self.exists(key):
            try:
                self.client.delete(key)
                return True
            except redis.RedisError as e:
                # Handle or log Redis errors
                print(f"Error deleting key {key}: {e}")
        return False
