"""Worker tests"""
import pytest
from pyre.worker import Worker
from pyre.task import Task, TaskStatus
from pyre.resource import ResourceManager

class TestWorker:
    def test_execute(self):
        rm = ResourceManager()
        worker = Worker(0, rm)
        task = Task(name="test", func=lambda: 42)
        result = worker.execute(task)
        assert result == True
        assert task.status == TaskStatus.COMPLETED
        assert task.result == 42
    
    def test_is_idle(self):
        rm = ResourceManager()
        worker = Worker(0, rm)
        assert worker.is_idle == True
