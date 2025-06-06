import time
import functools
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics.metrics_collector import MetricsCollector

# Global metrics collector instance
_collector = MetricsCollector()

def time_llm_task(task_name=None):
    """
    Decorator to measure LLM processing time for a function.
    
    Args:
        task_name: Name of the task. If None, uses the function name.
    
    Returns:
        Decorated function that records processing time.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get task name
            nonlocal task_name
            if task_name is None:
                task_name = func.__name__
            
            # Record start time
            start_time = time.time()
            
            # Execute the function
            result = func(*args, **kwargs)
            
            # Record end time
            end_time = time.time()
            
            # Extract token information if available
            tokens_in = kwargs.get('tokens_in', None)
            tokens_out = None
            
            # Try to extract tokens_out from result if it's a dict
            if isinstance(result, dict) and 'tokens_out' in result:
                tokens_out = result['tokens_out']
            
            # Record the processing time
            _collector.record_llm_processing_time(
                task_name, 
                start_time, 
                end_time,
                tokens_in,
                tokens_out
            )
            
            return result
        return wrapper
    return decorator

def get_metrics_collector():
    """Get the global metrics collector instance"""
    return _collector

# Example of direct timing (for use in blocks of code)
class TimeLLMTask:
    """Context manager to time LLM tasks"""
    
    def __init__(self, task_name, tokens_in=None):
        self.task_name = task_name
        self.tokens_in = tokens_in
        self.start_time = None
        self.tokens_out = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        _collector.record_llm_processing_time(
            self.task_name,
            self.start_time,
            end_time,
            self.tokens_in,
            self.tokens_out
        )
        
    def set_tokens_out(self, tokens_out):
        """Set the number of output tokens"""
        self.tokens_out = tokens_out
