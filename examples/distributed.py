#!/usr/bin/env python3
"""Distributed execution example"""
from pyre import Scheduler, Task, Resource

def process_data(chunk_id: int):
    """Process data chunk"""
    return {"chunk": chunk_id, "processed": True}

def main():
    scheduler = Scheduler(num_workers=8)
    
    # Submit parallel tasks
    tasks = [
        Task(name=f"process_{i}", func=process_data, args={"chunk_id": i})
        for i in range(100)
    ]
    
    job_ids = scheduler.submit_batch(tasks)
    print(f"Submitted {len(job_ids)} tasks")
    
    # Monitor progress
    completed = sum(1 for jid in job_ids 
                   if scheduler.status(jid) == TaskStatus.COMPLETED)
    print(f"Completed: {completed}/{len(job_ids)}")

if __name__ == "__main__":
    main()
