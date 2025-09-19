import functools
import time

def retry_on_failure(retries=3, delay=2):
    """Retry the function if it raises an exception"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            raise Exception(f"Failed after {retries} attempts")
        return wrapper
    return decorator
