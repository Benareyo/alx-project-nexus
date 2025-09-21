import pytest
from async_context.execute import ExecuteQuery

def test_execute_query():
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", [25]) as cursor:
        results = cursor.fetchall()
    assert all(user['age'] > 25 for user in results), "All users should be older than 25"
