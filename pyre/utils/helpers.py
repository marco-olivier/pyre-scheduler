"""Helper functions"""
from typing import Union

def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

def parse_size(size_str: str) -> int:
    """Parse size string to bytes"""
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
    for unit, mult in units.items():
        if size_str.upper().endswith(unit):
            return int(size_str[:-len(unit)]) * mult
    return int(size_str)

def generate_id() -> str:
    """Generate unique ID"""
    import uuid
    return str(uuid.uuid4())[:8]
