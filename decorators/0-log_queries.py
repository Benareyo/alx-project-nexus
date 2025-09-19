import functools

def log_queries(func):
    """
    Logs the SQL query before executing the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", "")
        print(f"🔹 Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper
