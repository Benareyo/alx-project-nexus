import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or []

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()  # save changes if any
        self.conn.close()   # always close the connection

# --- Example usage ---
with ExecuteQuery("SELECT * FROM users WHERE age > ?", [25]) as cursor:
    results = cursor.fetchall()
    print(results)
