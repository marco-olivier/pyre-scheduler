"""Metrics storage"""
from typing import Dict, List
from dataclasses import dataclass
import time

@dataclass
class MetricPoint:
    """Single metric measurement"""
    timestamp: float
    value: float
    labels: Dict[str, str]

class MetricsStore:
    """Time-series metrics storage"""
    
    def __init__(self, max_points: int = 10000):
        self._metrics: Dict[str, List[MetricPoint]] = {}
        self._max_points = max_points
    
    def record(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record metric"""
        if name not in self._metrics:
            self._metrics[name] = []
        
        point = MetricPoint(
            timestamp=time.time(),
            value=value,
            labels=labels or {}
        )
        self._metrics[name].append(point)
        
        # Trim old points
        if len(self._metrics[name]) > self._max_points:
            self._metrics[name] = self._metrics[name][-self._max_points:]
    
    def query(self, name: str, start: float = 0, end: float = float('inf')) -> List[MetricPoint]:
        """Query metrics"""
        if name not in self._metrics:
            return []
        return [p for p in self._metrics[name] if start <= p.timestamp <= end]
    
    def get_latest(self, name: str) -> float:
        """Get latest metric value"""
        if name not in self._metrics or not self._metrics[name]:
            return 0.0
        return self._metrics[name][-1].value
