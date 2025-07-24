import threading
import flet as ft
from enum import Enum
from typing import Callable

from app.db.mongo import get_collection
from app.db.sqlite import connect_to_sqlite, find_user_sqlite, insert_user_sqlite, DBKey
from app.ui.screens.loading_screen import show_loading_screen


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
        return get_collection().find_one({DBKey.USERNAME.value: username})
    else:
        conn = connect_to_sqlite()
        return find_user_sqlite(conn, username)

def insert_user(username: str, hashed_password: str, op: bool = False):
    if db_mode[mode] == DBMode.MONGO:
        get_collection().insert_one({
            DBKey.USERNAME.value: username,
            DBKey.PASSWORD.value: hashed_password,
            DBKey.OP.value: op
        })
    else:
        conn = connect_to_sqlite()
        insert_user_sqlite(conn, username, hashed_password, op)

def update_user(filter_query: dict, updated_fields: dict) -> bool:
    """
    Update a user document in the collection.

    Args:
        filter_query (dict): The filter used to find the document (e.g. {"_id": ObjectId(id)} or {"email": "example@example.com"})
        updated_fields (dict): Dictionary of fields to update

    Returns:
        bool: True if the update matched a document, False otherwise
    """
    update_payload = {"$set": updated_fields}
    result = get_collection().update_one(filter_query, update_payload)
    return result.matched_count > 0

def check_matching_document(filter_query: dict, value_checks: dict = None) -> bool:
    """
    Check if a document matching `filter_query` exists and optionally validate individual fields.

    Args:
        filter_query (dict): MongoDB query to find the document.
        value_checks (dict, optional): Specific field:value pairs to check inside the found document.

    Returns:
        bool: True if matching document and all specified fields match, else False.
    """
    doc = get_collection().find_one(filter_query)
    if not doc:
        return False

    if value_checks:
        for key, expected_value in value_checks.items():
            if doc.get(key) != expected_value:
                return False

    return True

def init_database(page: ft.Page = None, callback: Callable = None):
    global collection, sqlite_conn, initialized
    print(f"init_database() Called with mode={db_mode[mode].value}, initialized={initialized}")

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
