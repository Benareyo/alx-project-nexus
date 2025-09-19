# setup_db.py
import sqlite3

# Connect to a SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create a table called 'users' if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

# Insert some sample data
sample_users = [
    ("Alice", 30),
    ("Bob", 45),
    ("Charlie", 22),
    ("Diana", 55),
    ("Ethan", 40)
]

# Insert data only if the table is empty
cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", sample_users)
    print("Sample data inserted.")
else:
    print("Users table already has data, skipping insert.")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup complete.")
