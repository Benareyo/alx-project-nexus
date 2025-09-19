import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Connect to MySQL
try:
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

    cursor = connection.cursor()

    # Sample users to seed into the DB
    users = [
        ("Sofia", "Abera", "sofia.abera@example.com"),
        ("Liam", "Tadesse", "liam.tadesse@example.com"),
        ("Maya", "Kassa", "maya.kassa@example.com"),
        ("Noah", "Hailu", "noah.hailu@example.com"),
        ("Zoe", "Bekele", "zoe.bekele@example.com")
    ]

    # Insert data
    cursor.executemany(
        "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)",
        users
    )
    connection.commit()

    print("✅ Users seeded successfully!")

except Error as e:
    print(f"❌ Error: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
