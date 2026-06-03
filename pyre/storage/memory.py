"""In-memory storage"""
from typing import Dict, Optional, List
from ..task import Task, TaskStatus

class MemoryStorage:
    """In-memory task storage"""
    
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
    
    def save(self, task: Task):
        """Save task"""
        self._tasks[task.id] = task
    
    def load(self, task_id: str) -> Optional[Task]:
        """Load task"""
        return self._tasks.get(task_id)
    
    def delete(self, task_id: str):
        """Delete task"""
        self._tasks.pop(task_id, None)
    
    def list_all(self) -> List[Task]:
        """List all tasks"""
        return list(self._tasks.values())
    
    def list_by_status(self, status: TaskStatus) -> List[Task]:
        """List tasks by status"""
        return [t for t in self._tasks.values() if t.status == status]
    
    def count(self) -> int:
        """Count tasks"""
        return len(self._tasks)
