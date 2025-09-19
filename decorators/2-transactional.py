import functools

def transactional(func):
    """Decorator to wrap a function inside a DB transaction"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed, rolled back: {e}")
            raise
    return wrapper
