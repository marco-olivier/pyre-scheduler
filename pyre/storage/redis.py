"""Redis storage backend"""
from typing import Optional, List
import json

class RedisStorage:
    """Redis-backed task storage"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self._redis_url = redis_url
        self._client = None
        self._prefix = "pyre:"
    
    def _connect(self):
        """Connect to Redis"""
        if self._client is None:
            import redis
            self._client = redis.from_url(self._redis_url)
    
    def save(self, task):
        """Save task to Redis"""
        self._connect()
        key = f"{self._prefix}task:{task.id}"
        data = json.dumps({
            'id': task.id,
            'name': task.name,
            'status': task.status.value,
            'args': task.args,
        })
        self._client.set(key, data)
    
    def load(self, task_id: str):
        """Load task from Redis"""
        self._connect()
        key = f"{self._prefix}task:{task_id}"
        data = self._client.get(key)
        if data:
            return json.loads(data)
        return None
    
    def delete(self, task_id: str):
        """Delete task"""
        self._connect()
        key = f"{self._prefix}task:{task_id}"
        self._client.delete(key)
    
    def list_all(self) -> List[dict]:
        """List all tasks"""
        self._connect()
        keys = self._client.keys(f"{self._prefix}task:*")
        tasks = []
        for key in keys:
            data = self._client.get(key)
            if data:
                tasks.append(json.loads(data))
        return tasks
