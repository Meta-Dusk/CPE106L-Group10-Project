from db.mongo import connect_to_mongo
from db.sqlite import connect_to_sqlite, find_user_sqlite, insert_user_sqlite
from constants import DBMode

mode = "mode"
username = "username"
password = "password"
db_mode = {mode: DBMode.MONGO} # Default db: MongoDB
collection = None
sqlite_conn = None

def init_database():
    global collection, sqlite_conn
    if db_mode[mode] == DBMode.MONGO:
        collection = connect_to_mongo()
        return collection is not None
    else:
        sqlite_conn = connect_to_sqlite()
        return sqlite_conn is not None

def toggle_db():
    db_mode[mode] = DBMode.SQLITE if db_mode[mode] == DBMode.MONGO else DBMode.MONGO
    return db_mode[mode]

def get_current_mode():
    return db_mode[mode]

def find_user(username):
    if db_mode[mode] == DBMode.MONGO:
        return collection.find_one({username: username})
    else:
        return find_user_sqlite(sqlite_conn, username)

def insert_user(username, hashed_password):
    if db_mode[mode] == DBMode.MONGO:
        collection.insert_one({username: username, password: hashed_password})
    else:
        insert_user_sqlite(sqlite_conn, username, hashed_password)
