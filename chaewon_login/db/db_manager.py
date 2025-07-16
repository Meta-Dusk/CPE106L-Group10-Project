import threading

from chaewon_login.db.mongo import connect_to_mongo, get_collection
from chaewon_login.db.sqlite import connect_to_sqlite, find_user_sqlite, insert_user_sqlite, get_sqlite_conn
from chaewon_login.ui.loading_screen import show_loading_screen
from enum import Enum

class DBMode(Enum):
    MONGO = "MongoDB"
    SQLITE = "SQLite"

mode = "mode"
db_mode = {mode: DBMode.MONGO} # Default db: MongoDB
collection = None
sqlite_conn = None
initialized = False

def toggle_db():
    global collection, sqlite_conn
    msg = f"Toggling database mode from {db_mode[mode].value} to "
    db_mode[mode] = DBMode.SQLITE if db_mode[mode] == DBMode.MONGO else DBMode.MONGO
    msg += f"{db_mode[mode].value}"
    print(msg)
        
    return db_mode[mode]

def get_current_mode():
    return db_mode[mode]

def find_user(username):
    if db_mode[mode] == DBMode.MONGO:
        return get_collection().find_one({"username": username})
    else:
        return find_user_sqlite(get_sqlite_conn(), username)

def insert_user(username, hashed_password):
    if db_mode[mode] == DBMode.MONGO:
        get_collection().insert_one({"username": username, "password": hashed_password})
    else:
        insert_user_sqlite(get_sqlite_conn(), username, hashed_password)

def init_database(page=None):
    global collection, sqlite_conn, initialized

    if initialized:
        return collection if db_mode[mode] == DBMode.MONGO else sqlite_conn

    if page:
        show_loading_screen(page, f"Connecting to {db_mode[mode].value}...")

        def db_init():
            global collection, sqlite_conn, initialized
            collection = connect_to_mongo()
            sqlite_conn = connect_to_sqlite()
            initialized = True
            # Clear loading screen and refresh the main UI
            page.controls.clear()
            page.overlay.clear()
            page.update()
            # Call the login UI again or your intended next screen
            from chaewon_login.ui.login_ui import main_login_ui
            main_login_ui(page)

        threading.Thread(target=db_init).start()
        return None  # Since we don’t have the DB yet

    # Fallback for when no page is passed
    collection = connect_to_mongo()
    sqlite_conn = connect_to_sqlite()
    initialized = True
    return collection if db_mode[mode] == DBMode.MONGO else sqlite_conn


def test():
    print("Database switching test...\n")
    print(f"Current DBMode: {get_current_mode().value}\n")
    init_database()
    print("\nTime to switch.\n")
    toggle_db()

if __name__ == "__main__":
    test()