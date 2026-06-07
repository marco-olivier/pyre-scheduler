# Getting Started

## Installation

```bash
pip install pyre-scheduler
```

## Quick Start

```python
from pyre import Scheduler, Task

scheduler = Scheduler()
task = Task(name="my_task", func=my_function, args={"param": 1})
job_id = scheduler.submit(task)
```

## Configuration

```python
from pyre.scheduler import SchedulerConfig

config = SchedulerConfig(
    num_workers=8,
    max_retries=3,
    task_timeout=3600
)
scheduler = Scheduler(config=config)
```
