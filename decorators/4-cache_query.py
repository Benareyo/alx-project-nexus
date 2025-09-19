import functools

query_cache = {}

def cache_query(func):
    """Caches query results based on the SQL string"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else "")
        if query in query_cache:
            print("Using cached result")
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper
