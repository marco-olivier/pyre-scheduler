"""Task planning and dependency resolution"""
from typing import List, Dict, Set
from .task import Task, TaskStatus
from collections import defaultdict, deque

class Planner:
    """Task planner with dependency resolution"""
    
    def __init__(self):
        self._dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self._reverse_graph: Dict[str, Set[str]] = defaultdict(set)
    
    def add_task(self, task: Task):
        """Register task with its dependencies"""
        for dep_id in task.dependencies:
            self._dependency_graph[task.id].add(dep_id)
            self._reverse_graph[dep_id].add(task.id)
    
    def get_ready_tasks(self, completed: Set[str]) -> List[str]:
        """Get tasks whose dependencies are satisfied"""
        ready = []
        for task_id, deps in self._dependency_graph.items():
            if deps.issubset(completed) and task_id not in completed:
                ready.append(task_id)
        return ready
    
    def get_execution_order(self) -> List[str]:
        """Topological sort of tasks"""
        in_degree = defaultdict(int)
        for task_id in self._dependency_graph:
            in_degree[task_id] = len(self._dependency_graph[task_id])
        
        queue = deque([t for t in in_degree if in_degree[t] == 0])
        order = []
        
        while queue:
            task_id = queue.popleft()
            order.append(task_id)
            for dependent in self._reverse_graph[task_id]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        return order
    
    def has_cycles(self) -> bool:
        """Check for circular dependencies"""
        try:
            self.get_execution_order()
            return False
        except ValueError:
            return True
