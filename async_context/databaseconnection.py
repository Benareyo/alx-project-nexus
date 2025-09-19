# 0-databaseconnection.py
import sqlite3

class DatabaseConnection:
    def __init__(self, db_file="bridal.db"):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row  # makes rows act like dictionaries
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"An error happened: {exc_val}")
        return False  # if error, show it

# Example usage
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            print(dict(row))
