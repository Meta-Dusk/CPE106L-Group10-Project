import sqlite3

database_name = "accounts"

def connect_to_sqlite():
    conn = sqlite3.connect(f"{database_name}.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    print("Connected to SQLite and 'accounts' table is ready.")
    return conn

def find_user_sqlite(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    row = cursor.fetchone()
    return dict(row) if row else None


def insert_user_sqlite(conn, username, hashed_password):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

""" Run sqlite.py to test database connection and table creation """
def main():
    with connect_to_sqlite() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM accounts LIMIT 1;")
        result = cursor.fetchone()

        if result:
            print("Table has at least one entry.")
            cursor.execute(f"SELECT username FROM accounts ORDER BY RANDOM() LIMIT 1;")
            result = cursor.fetchone()
            random_username = result["username"]
            print(f'Such as user "{random_username}"')
        else:
            print("Table is empty.")
    
if __name__ == "__main__":
    main()