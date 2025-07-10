import sqlite3

def connect_to_sqlite():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

def find_user_sqlite(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM accounts WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        return {"username": row[0], "password": row[1]}
    return None

def insert_user_sqlite(conn, username, hashed_password):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
