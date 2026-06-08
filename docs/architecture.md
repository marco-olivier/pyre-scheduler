# Architecture

## Components

### Scheduler
Main entry point for task submission and management.

### TaskQueue
Priority-based queue with O(log n) operations.

### Planner
Dependency resolution using topological sort.

### ResourceManager
Tracks and allocates GPU/CPU resources.

### Worker
Executes tasks with resource isolation.

## Data Flow

1. Client submits task
2. Scheduler adds to queue
3. Planner resolves dependencies
4. Resource manager allocates resources
5. Worker executes task
6. Results stored and returned

## Scaling

- Single node: in-process workers
- Distributed: Redis-backed queue with multiple nodes
