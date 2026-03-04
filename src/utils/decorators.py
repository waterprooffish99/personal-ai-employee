import time
import functools
from typing import Callable, Any, Type
import logging
from .logger import log_action

def with_retry(max_retries: int = 3, backoff_factor: float = 2.0, exceptions: tuple = (Exception,)) -> Callable:
    """
    Decorator for exponential backoff and graceful degradation.
    
    Args:
        max_retries: Maximum number of retries before giving up.
        backoff_factor: Multiplier for the delay between retries.
        exceptions: Tuple of exceptions to catch and retry on.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            delay = 1.0  # Initial delay in seconds
            
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        log_action(
                            f"Function {func.__name__} failed after {max_retries} retries.",
                            actor="system",
                            result="error",
                            details={"error": str(e)}
                        )
                        raise
                    
                    log_action(
                        f"Function {func.__name__} failed. Retrying in {delay} seconds...",
                        actor="system",
                        result="warning",
                        details={"error": str(e), "retry": retries}
                    )
                    time.sleep(delay)
                    delay *= backoff_factor
        return wrapper
    return decorator
