"""Resource tests"""
import pytest
from pyre.resource import Resource, ResourceManager

class TestResource:
    def test_parse_size(self):
        assert Resource._parse_size("1GB") == 1024**3
        assert Resource._parse_size("512MB") == 512 * 1024**2
    
    def test_resource_manager(self):
        rm = ResourceManager()
        r = Resource(cpu=2, memory="4GB", gpu=1)
        alloc_id = rm.allocate(r)
        assert alloc_id is not None
        rm.release(alloc_id)
