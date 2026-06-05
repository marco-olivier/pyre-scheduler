"""Queue tests"""
import pytest
from pyre.queue import TaskQueue
from pyre.task import Task

class TestTaskQueue:
    def test_enqueue_dequeue(self):
        queue = TaskQueue()
        task = Task(name="test", func=lambda: None)
        queue.enqueue(task)
        result = queue.dequeue()
        assert result.name == "test"
    
    def test_priority(self):
        queue = TaskQueue()
        low = Task(name="low", func=lambda: None, priority=1)
        high = Task(name="high", func=lambda: None, priority=10)
        queue.enqueue(low)
        queue.enqueue(high)
        assert queue.dequeue().name == "high"
    
    def test_empty(self):
        queue = TaskQueue()
        assert queue.dequeue() is None
