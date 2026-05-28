"""Core scheduler"""
from typing import Optional, Dict, List, Callable
from .task import Task, TaskStatus
from .queue import TaskQueue
from .planner import Planner
from .resource import ResourceManager
import uuid

class SchedulerConfig:
    """Scheduler configuration"""
    def __init__(self, num_workers: int = 4, max_retries: int = 3,
                 task_timeout: int = 3600, enable_gpu: bool = True):
        self.num_workers = num_workers
        self.max_retries = max_retries
        self.task_timeout = task_timeout
        self.enable_gpu = enable_gpu

class Scheduler:
    """Main scheduler interface"""
    
    def __init__(self, config: Optional[SchedulerConfig] = None):
        self.config = config or SchedulerConfig()
        self._queue = TaskQueue()
        self._planner = Planner()
        self._resource_manager = ResourceManager()
        self._tasks: Dict[str, Task] = {}
        self._workers = []
        self._running = False
    
    def submit(self, task: Task) -> str:
        """Submit task for execution"""
        task_id = str(uuid.uuid4())[:8]
        task.id = task_id
        task.status = TaskStatus.PENDING
        self._tasks[task_id] = task
        self._queue.enqueue(task)
        return task_id
    
    def submit_batch(self, tasks: List[Task]) -> List[str]:
        """Submit multiple tasks"""
        return [self.submit(task) for task in tasks]
    
    def status(self, task_id: str) -> TaskStatus:
        """Get task status"""
        if task_id not in self._tasks:
            raise ValueError(f"Task not found: {task_id}")
        return self._tasks[task_id].status
    
    def cancel(self, task_id: str):
        """Cancel task"""
        if task_id in self._tasks:
            self._tasks[task_id].status = TaskStatus.CANCELLED
    
    def get_result(self, task_id: str):
        """Get task result"""
        task = self._tasks.get(task_id)
        if task and task.status == TaskStatus.COMPLETED:
            return task.result
        return None
    
    def start(self):
        """Start scheduler"""
        self._running = True
    
    def stop(self):
        """Stop scheduler"""
        self._running = False
    
    def _process_next(self):
        """Process next task from queue"""
        task = self._queue.dequeue()
        if task:
            # Allocate resources
            resources = self._resource_manager.allocate(task.resources)
            if resources:
                task.status = TaskStatus.RUNNING
                # Execute task
                try:
                    result = task.func(**task.args)
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                except Exception as e:
                    task.error = str(e)
                    task.status = TaskStatus.FAILED
                finally:
                    self._resource_manager.release(resources)
