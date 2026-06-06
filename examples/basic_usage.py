#!/usr/bin/env python3
"""Basic usage example"""
from pyre import Scheduler, Task, Resource

def train_model(epochs: int, lr: float):
    """Example training function"""
    print(f"Training for {epochs} epochs with lr={lr}")
    return {"loss": 0.5, "accuracy": 0.95}

def main():
    scheduler = Scheduler()
    
    # Submit task
    task = Task(
        name="train_resnet",
        func=train_model,
        args={"epochs": 10, "lr": 0.001},
        resources=Resource(gpu=1, memory="8GB")
    )
    
    job_id = scheduler.submit(task)
    print(f"Submitted job: {job_id}")
    
    # Get result
    result = scheduler.get_result(job_id)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
