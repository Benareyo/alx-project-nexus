import sqlite3

DB_PATH = "async_context/test_users.db"  
def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute("DROP TABLE IF EXISTS users")

    # Create users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    # Insert some sample users
    users = [
        ("Alice", 30),
        ("Bob", 45),
        ("Charlie", 50),
        ("Diana", 20)
    ]
    cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)

    conn.commit()
    conn.close()
    print(f"Database setup complete! Table 'users' created in {DB_PATH}")

if __name__ == "__main__":
    setup_database()

