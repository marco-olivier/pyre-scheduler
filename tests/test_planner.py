"""Planner tests"""
import pytest
from pyre.planner import Planner
from pyre.task import Task

class TestPlanner:
    def test_execution_order(self):
        planner = Planner()
        t1 = Task(name="t1", func=lambda: None)
        t2 = Task(name="t2", func=lambda: None, dependencies=[t1.id])
        planner.add_task(t1)
        planner.add_task(t2)
        order = planner.get_execution_order()
        assert order.index(t1.id) < order.index(t2.id)
    
    def test_no_cycles(self):
        planner = Planner()
        assert planner.has_cycles() == False
