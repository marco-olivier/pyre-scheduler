"""Job monitoring and status tracking"""
from typing import Dict, List, Optional
from ..task import Task, TaskStatus
import time

class JobInfo:
    """Job information"""
    def __init__(self, task: Task):
        self.task = task
        self.start_time = time.time()
        self.end_time: Optional[float] = None
    
    @property
    def duration(self) -> float:
        end = self.end_time or time.time()
        return end - self.start_time

class JobMonitor:
    """Monitor job execution"""
    
    def __init__(self):
        self._jobs: Dict[str, JobInfo] = {}
        self._history: List[JobInfo] = []
    
    def track(self, task: Task):
        """Start tracking job"""
        self._jobs[task.id] = JobInfo(task)
    
    def complete(self, task_id: str):
        """Mark job as complete"""
        if task_id in self._jobs:
            job = self._jobs.pop(task_id)
            job.end_time = time.time()
            self._history.append(job)
    
    def get_active_jobs(self) -> List[JobInfo]:
        """Get currently running jobs"""
        return list(self._jobs.values())
    
    def get_history(self, limit: int = 100) -> List[JobInfo]:
        """Get job history"""
        return self._history[-limit:]
    
    def get_stats(self) -> Dict:
        """Get job statistics"""
        completed = [j for j in self._history if j.task.status == TaskStatus.COMPLETED]
        failed = [j for j in self._history if j.task.status == TaskStatus.FAILED]
        
        return {
            'active': len(self._jobs),
            'completed': len(completed),
            'failed': len(failed),
            'avg_duration': sum(j.duration for j in completed) / max(len(completed), 1),
        }
