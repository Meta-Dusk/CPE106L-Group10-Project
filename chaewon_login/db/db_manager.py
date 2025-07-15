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
    print(f"Toggling database mode from {db_mode[mode].value} to:")
    db_mode[mode] = DBMode.SQLITE if db_mode[mode] == DBMode.MONGO else DBMode.MONGO
    print(f"{db_mode[mode].value}")

    # Clear old connections to force reconnect
    collection = None
    sqlite_conn = None

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

    if db_mode[mode] == DBMode.MONGO:
        collection = connect_to_mongo()
    else:
        sqlite_conn = connect_to_sqlite()

    initialized = True
    return collection if db_mode[mode] == DBMode.MONGO else sqlite_conn
