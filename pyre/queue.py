"""Task queue implementation"""
from typing import Optional, List
from .task import Task
import heapq
import threading

class TaskQueue:
    """Priority-based task queue"""
    
    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()
        self._task_map = {}
    
    def enqueue(self, task: Task):
        """Add task to queue"""
        with self._lock:
            # Use negative priority for max-heap
            heapq.heappush(self._queue, (-task.priority, task.id, task))
            self._task_map[task.id] = task
    
    def dequeue(self) -> Optional[Task]:
        """Get highest priority task"""
        with self._lock:
            if self._queue:
                _, _, task = heapq.heappop(self._queue)
                del self._task_map[task.id]
                return task
            return None
    
    def peek(self) -> Optional[Task]:
        """Look at next task without removing"""
        with self._lock:
            if self._queue:
                return self._queue[0][2]
            return None
    
    def remove(self, task_id: str) -> bool:
        """Remove task from queue"""
        with self._lock:
            if task_id in self._task_map:
                del self._task_map[task_id]
                # Rebuild queue without this task
                self._queue = [(p, t.id, t) for p, _, t in self._queue if t.id != task_id]
                heapq.heapify(self._queue)
                return True
            return False
    
    @property
    def size(self) -> int:
        return len(self._queue)
    
    @property
    def is_empty(self) -> bool:
        return len(self._queue) == 0
    
    def get_all(self) -> List[Task]:
        """Get all tasks in queue"""
        with self._lock:
            return [t for _, _, t in sorted(self._queue)]
