"""Task pipeline with chaining"""
from typing import List, Callable, Any
from .task import Task
from .scheduler import Scheduler

class Pipeline:
    """Chain tasks into a pipeline"""
    
    def __init__(self, name: str, scheduler: Scheduler):
        self.name = name
        self.scheduler = scheduler
        self._stages: List[dict] = []
    
    def add_stage(self, name: str, func: Callable, **kwargs) -> 'Pipeline':
        """Add pipeline stage"""
        self._stages.append({
            'name': name,
            'func': func,
            'args': kwargs
        })
        return self
    
    def execute(self, initial_input: Any = None) -> Any:
        """Execute pipeline"""
        result = initial_input
        
        for stage in self._stages:
            task = Task(
                name=f"{self.name}_{stage['name']}",
                func=stage['func'],
                args={**stage['args'], 'input': result}
            )
            job_id = self.scheduler.submit(task)
            result = self.scheduler.get_result(job_id)
        
        return result
    
    def execute_parallel(self, inputs: List[Any]) -> List[Any]:
        """Execute pipeline for multiple inputs"""
        jobs = []
        for inp in inputs:
            task = Task(
                name=f"{self.name}_batch",
                func=self._execute_chain,
                args={'input': inp}
            )
            job_id = self.scheduler.submit(task)
            jobs.append(job_id)
        
        return [self.scheduler.get_result(jid) for jid in jobs]
    
    def _execute_chain(self, input):
        """Execute all stages in sequence"""
        result = input
        for stage in self._stages:
            result = stage['func'](result, **stage['args'])
        return result
