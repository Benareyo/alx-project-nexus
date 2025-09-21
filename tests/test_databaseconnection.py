import pytest
from async_context.databaseconnection import DatabaseConnection

def test_db_connection():
    # Open database connection using context manager
    with DatabaseConnection("async_context/test_db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        table_exists = cursor.fetchone()
    assert table_exists is not None, "Users table should exist"
