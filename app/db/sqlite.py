import sqlite3
from pathlib import Path
from enum import Enum

class DBKey(Enum):
    USERNAME = "username"
    PASSWORD = "password"
    OP = "op"

TABLE_NAME = "accounts"
DB_NAME = "ATS_Data"
DB_DIR = Path(__file__).parent / "data"
DB_PATH = DB_DIR / f"{DB_NAME}.db"

def connect_to_sqlite():
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {DBKey.USERNAME.value} TEXT PRIMARY KEY,
            {DBKey.PASSWORD.value} TEXT NOT NULL,
            {DBKey.OP.value} BOOL NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    print(f"Connected to SQLite and {TABLE_NAME} table is ready.")
    return conn

def find_user_sqlite(conn, username: str):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE {DBKey.USERNAME.value} = ?", (username,))
    row = cursor.fetchone()
    return dict(row) if row else None


def insert_user_sqlite(conn, username: str, hashed_password: str, op: bool = False):
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {TABLE_NAME} ({DBKey.USERNAME.value}, {DBKey.PASSWORD.value}, {DBKey.OP.value}) VALUES (?, ?, ?)
    """, (username, hashed_password, int(op)))
    conn.commit()


""" Run sqlite.py to test database connection and table creation """
def main():
    with connect_to_sqlite() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM {TABLE_NAME} LIMIT 1;")
        result = cursor.fetchone()

        if result:
            print("Table has at least one entry.")
            cursor.execute(f"SELECT {DBKey.USERNAME.value} FROM {TABLE_NAME} ORDER BY RANDOM() LIMIT 1;")
            result = cursor.fetchone()
            random_username = result[DBKey.USERNAME.value]
            print(f'Such as user "{random_username}"')
            cursor.execute(f"SELECT COUNT (*) FROM {TABLE_NAME}")
        else:
            print("Table is empty.")
    
if __name__ == "__main__":
    main()