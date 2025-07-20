import threading
from enum import Enum

from chaewon_login.db.mongo import get_collection
from chaewon_login.db.sqlite import connect_to_sqlite, find_user_sqlite, insert_user_sqlite
from chaewon_login.ui.screens.loading_screen import show_loading_screen
from typing import Callable


class DBMode(Enum):
    MONGO = "MongoDB"
    SQLITE = "SQLite"

mode = "mode"
db_mode = {mode: DBMode.MONGO}  # Default: MongoDB
collection = None
sqlite_conn = None
initialized = False


def toggle_db():
    global db_mode, collection, sqlite_conn, initialized
    old_mode = db_mode[mode]
    db_mode[mode] = DBMode.SQLITE if old_mode == DBMode.MONGO else DBMode.MONGO
    print(f"Toggled DB mode from {old_mode.value} to {db_mode[mode].value}")
    
    # Reset initialization state
    collection = None
    sqlite_conn = None
    initialized = False

    return db_mode[mode]

def get_current_mode():
    return db_mode[mode]

def find_user(username):
    if db_mode[mode] == DBMode.MONGO:
        return get_collection().find_one({"username": username})
    else:
        conn = connect_to_sqlite()
        return find_user_sqlite(conn, username)

def insert_user(username, hashed_password):
    if db_mode[mode] == DBMode.MONGO:
        get_collection().insert_one({"username": username, "password": hashed_password})
    else:
        conn = connect_to_sqlite()
        insert_user_sqlite(conn, username, hashed_password)

def init_database(page=None, callback: Callable=None):
    global collection, sqlite_conn, initialized
    print(f"`init_database()` Called with mode={db_mode[mode].value}, initialized={initialized}")

    if initialized:
        if callback:
            callback()
        return collection if db_mode[mode] == DBMode.MONGO else sqlite_conn

    def db_init():
        global collection, sqlite_conn, initialized

        if initialized:
            if callback:
                callback()
            return

        if db_mode[mode] == DBMode.MONGO:
            collection = get_collection()
        else:
            sqlite_conn = connect_to_sqlite()

        initialized = True

        if callback:
            callback()

    if page:
        show_loading_screen(page, f"Connecting to {db_mode[mode].value}...")
        threading.Thread(target=db_init).start()
        return None
    else:
        db_init()
        return collection if db_mode[mode] == DBMode.MONGO else sqlite_conn


def test():
    print("Database switching test...\n")
    print(f"Current DBMode: {get_current_mode().value}\n")
    init_database()
    print("\nTime to switch.\n")
    toggle_db()

if __name__ == "__main__":
    test()
