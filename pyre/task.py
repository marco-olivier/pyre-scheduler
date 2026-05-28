"""Task definition"""
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Task definition"""
    name: str
    func: Callable
    args: Dict[str, Any] = field(default_factory=dict)
    resources: Optional['Resource'] = None
    priority: int = 0
    max_retries: int = 3
    timeout: int = 3600
    dependencies: list = field(default_factory=list)
    
    # Runtime state
    id: str = ""
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    retries: int = 0
    
    def __post_init__(self):
        if self.resources is None:
            from .resource import Resource
            self.resources = Resource()

class TaskBuilder:
    """Builder pattern for tasks"""
    
    def __init__(self, name: str):
        self._task = Task(name=name, func=lambda: None)
    
    def with_func(self, func: Callable) -> 'TaskBuilder':
        self._task.func = func
        return self
    
    def with_args(self, **kwargs) -> 'TaskBuilder':
        self._task.args = kwargs
        return self
    
    def with_priority(self, priority: int) -> 'TaskBuilder':
        self._task.priority = priority
        return self
    
    def with_resources(self, resources) -> 'TaskBuilder':
        self._task.resources = resources
        return self
    
    def with_dependencies(self, *deps) -> 'TaskBuilder':
        self._task.dependencies = list(deps)
        return self
    
    def build(self) -> Task:
        return self._task
