"""Resource management"""
from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class Resource:
    """Resource requirements"""
    cpu: int = 1
    memory: str = "1GB"
    gpu: int = 0
    gpu_memory: str = "0GB"
    
    def __post_init__(self):
        self._memory_bytes = self._parse_size(self.memory)
        self._gpu_memory_bytes = self._parse_size(self.gpu_memory)
    
    @staticmethod
    def _parse_size(size_str: str) -> int:
        """Parse size string to bytes"""
        units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
        for unit, multiplier in units.items():
            if size_str.upper().endswith(unit):
                return int(size_str[:-len(unit)]) * multiplier
        return 0

class ResourceManager:
    """Manage compute resources"""
    
    def __init__(self):
        self._total_cpu = 16
        self._total_memory = 64 * 1024**3  # 64GB
        self._total_gpu = 4
        self._available_cpu = self._total_cpu
        self._available_memory = self._total_memory
        self._available_gpu = self._total_gpu
        self._allocated: Dict[str, Resource] = {}
    
    def allocate(self, resource: Resource) -> Optional[str]:
        """Allocate resources"""
        if (resource.cpu > self._available_cpu or
            resource._memory_bytes > self._available_memory or
            resource.gpu > self._available_gpu):
            return None
        
        self._available_cpu -= resource.cpu
        self._available_memory -= resource._memory_bytes
        self._available_gpu -= resource.gpu
        
        import uuid
        alloc_id = str(uuid.uuid4())[:8]
        self._allocated[alloc_id] = resource
        return alloc_id
    
    def release(self, alloc_id: str):
        """Release allocated resources"""
        if alloc_id in self._allocated:
            resource = self._allocated.pop(alloc_id)
            self._available_cpu += resource.cpu
            self._available_memory += resource._memory_bytes
            self._available_gpu += resource.gpu
    
    @property
    def available(self) -> Dict[str, int]:
        """Get available resources"""
        return {
            'cpu': self._available_cpu,
            'memory': self._available_memory,
            'gpu': self._available_gpu,
        }
