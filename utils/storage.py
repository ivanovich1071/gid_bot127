import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        chat_id INTEGER UNIQUE,
        registration_name TEXT,
        age INTEGER,
        registration_city TEXT,
        requested_cities TEXT
    )
    """)
    conn.commit()
    conn.close()
