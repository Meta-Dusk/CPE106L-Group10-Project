from pymongo import MongoClient
from cryptography.fernet import Fernet
from chaewon_login.config import Config
# from chaewon_login.utils import where_am_i

collection = None

def load_key():
    # print(f"Function `load_key()` was called in {where_am_i(2)}")
    print("🔓 Loading encryption key and decrypting MongoDB URI...")

    key = Config.KEY_PATH.read_bytes()
    fernet = Fernet(key)

    encrypted = Config.ENC_PATH.read_bytes()
    decrypted_uri = fernet.decrypt(encrypted).decode()

    print("✅ Decrypted MongoDB URI successfully.")
    return decrypted_uri

def connect_to_mongo():
    # print(f"Function `connect_to_mongo()` was called in {where_am_i(2)}")
    global collection
    if collection is not None:
        return collection

    try:
        uri = load_key()
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        db = client[Config.DB_NAME]
        print("✅ Connected to MongoDB.")
        collection = db[Config.COLLECTION_NAME]
        return collection
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
        return None

def get_collection():
    global collection
    if collection is None:
        collection = connect_to_mongo()
    return collection

"""
Run mongo.py to test database connection.
If in VSCode, you can run it with:
```Python
py -m chaewon_login.db.mongo
```
"""

def test():
    accounts_collection = connect_to_mongo()
    if accounts_collection is not None:
        print(f"📦 Collection '{Config.COLLECTION_NAME}' is ready.")
    else:
        print("🚫 Could not connect to MongoDB.")

if __name__ == "__main__":
    test()
