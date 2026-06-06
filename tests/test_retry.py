"""Retry tests"""
import pytest
from pyre.retry import RetryHandler, RetryConfig

class TestRetryHandler:
    def test_success(self):
        handler = RetryHandler()
        result = handler.execute_with_retry(lambda: 42)
        assert result == 42
    
    def test_retry_on_failure(self):
        call_count = 0
        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"
        
        handler = RetryHandler(RetryConfig(max_retries=3, base_delay=0.01))
        result = handler.execute_with_retry(failing_func)
        assert result == "success"
        assert call_count == 3
