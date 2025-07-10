from pymongo import MongoClient

MONGODB_CONNECTION_STRING = "localhost:27017"

def connect_to_mongo():
    try:
        client = MongoClient(f"mongodb://{MONGODB_CONNECTION_STRING}/", serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        db = client["ProjectATS"]
        return db["accounts"]
    except Exception as e:
        print("MongoDB connection failed:", e)
        return None
