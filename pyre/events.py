"""Event system for task lifecycle"""
from typing import Callable, Dict, List
from enum import Enum

class EventType(Enum):
    TASK_SUBMITTED = "task_submitted"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    TASK_CANCELLED = "task_cancelled"

class EventEmitter:
    """Event emitter for task lifecycle"""
    
    def __init__(self):
        self._handlers: Dict[EventType, List[Callable]] = {}
    
    def on(self, event: EventType, handler: Callable):
        """Register event handler"""
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)
    
    def emit(self, event: EventType, data: dict = None):
        """Emit event"""
        for handler in self._handlers.get(event, []):
            try:
                handler(data or {})
            except Exception as e:
                print(f"Event handler error: {e}")
    
    def off(self, event: EventType, handler: Callable):
        """Remove event handler"""
        if event in self._handlers:
            self._handlers[event].remove(handler)
