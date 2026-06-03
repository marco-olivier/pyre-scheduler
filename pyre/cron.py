"""Cron-like scheduled tasks"""
from typing import Callable, Optional
from dataclasses import dataclass
import time
import threading

@dataclass
class CronSchedule:
    """Cron schedule definition"""
    minute: str = "*"
    hour: str = "*"
    day: str = "*"
    month: str = "*"
    weekday: str = "*"

class CronJob:
    """Scheduled recurring task"""
    
    def __init__(self, name: str, func: Callable, schedule: CronSchedule,
                 args: dict = None):
        self.name = name
        self.func = func
        self.schedule = schedule
        self.args = args or {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
    
    def start(self):
        """Start cron job"""
        self._running = True
        self._thread = threading.Thread(target=self._run_loop)
        self._thread.start()
    
    def stop(self):
        """Stop cron job"""
        self._running = False
    
    def _run_loop(self):
        """Main execution loop"""
        while self._running:
            if self._should_run():
                try:
                    self.func(**self.args)
                except Exception as e:
                    print(f"Cron job {self.name} failed: {e}")
            time.sleep(60)  # Check every minute
    
    def _should_run(self) -> bool:
        """Check if job should run based on schedule"""
        # Simplified - just check if current minute matches
        return True

class CronScheduler:
    """Manage cron jobs"""
    
    def __init__(self):
        self._jobs: dict[str, CronJob] = {}
    
    def add_job(self, name: str, func: Callable, schedule: CronSchedule):
        """Add cron job"""
        self._jobs[name] = CronJob(name, func, schedule)
    
    def start_all(self):
        """Start all cron jobs"""
        for job in self._jobs.values():
            job.start()
    
    def stop_all(self):
        """Stop all cron jobs"""
        for job in self._jobs.values():
            job.stop()
