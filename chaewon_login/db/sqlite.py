import sqlite3
from pathlib import Path
from enum import Enum

class db_key(Enum):
    USERNAME = "username"
    PASSWORD = "password"

db_name = "accounts"
db_dir = Path(__file__).parent / "data"
db_path = db_dir / f"{db_name}.db"

def connect_to_sqlite():
    db_dir.mkdir(exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {db_name} (
            {db_key.USERNAME.value} TEXT PRIMARY KEY,
            {db_key.PASSWORD.value} TEXT NOT NULL
        )
    """)
    conn.commit()
    print(f"Connected to SQLite and {db_name} table is ready.")
    return conn

def find_user_sqlite(conn, username):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {db_name} WHERE {db_key.USERNAME.value} = ?", (username,))
    row = cursor.fetchone()
    return dict(row) if row else None


def insert_user_sqlite(conn, username, hashed_password):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {db_name} ({db_key.USERNAME.value}, {db_key.PASSWORD.value}) VALUES (?, ?)", (username, hashed_password))
    conn.commit()


""" Run sqlite.py to test database connection and table creation """
def main():
    with connect_to_sqlite() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM {db_name} LIMIT 1;")
        result = cursor.fetchone()

        if result:
            print("Table has at least one entry.")
            cursor.execute(f"SELECT {db_key.USERNAME.value} FROM {db_name} ORDER BY RANDOM() LIMIT 1;")
            result = cursor.fetchone()
            random_username = result["username"]
            print(f'Such as user "{random_username}"')
            cursor.execute(f"SELECT COUNT (*) FROM {db_name}")
        else:
            print("Table is empty.")
    
if __name__ == "__main__":
    main()