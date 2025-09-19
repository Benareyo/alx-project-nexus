import functools
import mysql.connector
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

def with_db_connection(func):
    """
    Opens a MySQL connection using environment variables,
    passes it to the function, and closes it automatically.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        try:
            result = func(connection, *args, **kwargs)
        finally:
            connection.close()
        return result
    return wrapper
