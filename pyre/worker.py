"""Worker implementation"""
from typing import Optional, Callable
from .task import Task, TaskStatus
from .resource import Resource, ResourceManager
import threading
import time

class WorkerState:
    IDLE = "idle"
    BUSY = "busy"
    STOPPED = "stopped"

class Worker:
    """Task execution worker"""
    
    def __init__(self, worker_id: int, resource_manager: ResourceManager):
        self.worker_id = worker_id
        self.resource_manager = resource_manager
        self.state = WorkerState.IDLE
        self.current_task: Optional[Task] = None
        self._thread: Optional[threading.Thread] = None
    
    def execute(self, task: Task) -> bool:
        """Execute task"""
        self.state = WorkerState.BUSY
        self.current_task = task
        task.status = TaskStatus.RUNNING
        
        try:
            # Allocate resources
            alloc_id = self.resource_manager.allocate(task.resources)
            if not alloc_id:
                task.status = TaskStatus.FAILED
                task.error = "Insufficient resources"
                return False
            
            # Execute
            result = task.func(**task.args)
            task.result = result
            task.status = TaskStatus.COMPLETED
            
            # Release resources
            self.resource_manager.release(alloc_id)
            return True
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            return False
        finally:
            self.state = WorkerState.IDLE
            self.current_task = None
    
    def execute_async(self, task: Task):
        """Execute task in background thread"""
        self._thread = threading.Thread(target=self.execute, args=(task,))
        self._thread.start()
    
    def stop(self):
        """Stop worker"""
        self.state = WorkerState.STOPPED
    
    @property
    def is_idle(self) -> bool:
        return self.state == WorkerState.IDLE
