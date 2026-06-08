# API Reference

## Scheduler

### `Scheduler(config=None)`
Create scheduler instance.

### `scheduler.submit(task) -> str`
Submit task for execution. Returns task ID.

### `scheduler.status(task_id) -> TaskStatus`
Get task status.

### `scheduler.cancel(task_id)`
Cancel pending/running task.

### `scheduler.get_result(task_id)`
Get task result (blocks until complete).

## Task

### `Task(name, func, args, resources, priority)`
Create task definition.

## Resource

### `Resource(cpu=1, memory="1GB", gpu=0, gpu_memory="0GB")`
Define resource requirements.

## Worker

### `Worker(worker_id, resource_manager)`
Create worker instance.

### `worker.execute(task) -> bool`
Execute task synchronously.
