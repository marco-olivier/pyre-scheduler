# Pyre Scheduler

Distributed task scheduler and job orchestration system for compute-intensive workloads.

## Features

- **Task Scheduling**: Priority-based task queuing
- **Distributed Execution**: Scale across multiple nodes
- **Resource Management**: GPU/CPU resource allocation
- **Dependency Resolution**: DAG-based task dependencies
- **Fault Tolerance**: Automatic retry and failover
- **Monitoring**: Real-time job status tracking

## Architecture

```
┌─────────────────────────────────────────┐
│             Client API                  │
├─────────────────────────────────────────┤
│           Scheduler Core                │
├──────────┬──────────┬───────────────────┤
│  Queue   │ Planner  │ Resource Manager  │
├──────────┴──────────┴───────────────────┤
│          Worker Pool                    │
├─────────┬─────────┬─────────────────────┤
│ Worker1 │ Worker2 │ WorkerN             │
└─────────┴─────────┴─────────────────────┘
```

## Quick Start

```python
from pyre import Scheduler, Task, Resource

# Create scheduler
scheduler = Scheduler(num_workers=4)

# Define task
task = Task(
    name="train_model",
    func=train_function,
    args={"epochs": 10},
    resources=Resource(gpu=1, memory="8GB")
)

# Submit task
job_id = scheduler.submit(task)

# Monitor
status = scheduler.status(job_id)
print(f"Job {job_id}: {status}")
```

## Requirements

- Python 3.9+
- Redis (for distributed mode)
- GPU drivers (for GPU tasks)

## Installation

```bash
pip install pyre-scheduler
```

## License

MIT License
