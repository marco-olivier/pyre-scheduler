"""Scheduler tests"""
import pytest
from pyre.scheduler import Scheduler
from pyre.task import Task, TaskStatus
from pyre.resource import Resource

class TestScheduler:
    def test_submit(self):
        scheduler = Scheduler()
        task = Task(name="test", func=lambda: 42)
        task_id = scheduler.submit(task)
        assert task_id is not None
        assert scheduler.status(task_id) == TaskStatus.PENDING
    
    def test_cancel(self):
        scheduler = Scheduler()
        task = Task(name="test", func=lambda: 42)
        task_id = scheduler.submit(task)
        scheduler.cancel(task_id)
        assert scheduler.status(task_id) == TaskStatus.CANCELLED
    
    def test_batch_submit(self):
        scheduler = Scheduler()
        tasks = [Task(name=f"task_{i}", func=lambda i=i: i) for i in range(5)]
        ids = scheduler.submit_batch(tasks)
        assert len(ids) == 5
