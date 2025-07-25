import sqlite3
from pathlib import Path
from enum import Enum

class DBKey(Enum):
    USERNAME = "username"
    PASSWORD = "password"
    OP = "op"
    ADDRESS = "address"
    DATE_OF_BIRTH = "date_of_birth"
    EMAIL = "email"
    FULL_NAME = "full_name"
    PHONE = "phone"
    

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
            {DBKey.OP.value} BOOL NOT NULL DEFAULT 0,
            {DBKey.ADDRESS.value} TEXT NOT NULL DEFAULT "",
            {DBKey.DATE_OF_BIRTH.value} TEXT NOT NULL DEFAULT "",
            {DBKey.EMAIL.value} TEXT NOT NULL DEFAULT "",
            {DBKey.FULL_NAME.value} TEXT NOT NULL DEFAULT "",
            {DBKey.PHONE.value} TEXT NOT NULL DEFAULT ""
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

def update_user_sqlite(conn, filter_query: dict, updated_fields: dict) -> bool:
    cursor = conn.cursor()

    # Generate WHERE clause
    where_clause = " AND ".join([f"{key} = ?" for key in filter_query])
    where_values = list(filter_query.values())

    # Generate SET clause
    set_clause = ", ".join([f"{key} = ?" for key in updated_fields])
    set_values = list(updated_fields.values())

    query = f"""
        UPDATE {TABLE_NAME}
        SET {set_clause}
        WHERE {where_clause}
    """

    cursor.execute(query, set_values + where_values)
    conn.commit()
    return cursor.rowcount > 0

def check_matching_document_sqlite(conn, filter_query: dict, value_checks: dict = None) -> bool:
    cursor = conn.cursor()

    where_clause = " AND ".join([f"{key} = ?" for key in filter_query])
    where_values = list(filter_query.values())

    cursor.execute(
        f"SELECT * FROM {TABLE_NAME} WHERE {where_clause}",
        where_values
    )

    row = cursor.fetchone()
    if not row:
        return False

    row_dict = dict(row)
    if value_checks:
        for key, expected_value in value_checks.items():
            if row_dict.get(key) != expected_value:
                return False

    return True



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