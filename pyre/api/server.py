"""REST API server"""
from typing import Dict, Any
from ..scheduler import Scheduler

def create_app(scheduler: Scheduler):
    """Create Flask/FastAPI app"""
    try:
        from fastapi import FastAPI
        app = FastAPI(title="Pyre Scheduler API")
    except ImportError:
        from flask import Flask
        app = Flask(__name__)
    
    @app.get("/health")
    def health():
        return {"status": "ok"}
    
    @app.get("/tasks")
    def list_tasks():
        return {"tasks": [t.id for t in scheduler._tasks.values()]}
    
    @app.get("/tasks/{task_id}")
    def get_task(task_id: str):
        task = scheduler._tasks.get(task_id)
        if task:
            return {"id": task.id, "status": task.status.value}
        return {"error": "not found"}, 404
    
    @app.post("/tasks")
    def submit_task(data: Dict[str, Any]):
        # Submit task
        return {"task_id": "new_task_id"}
    
    return app
