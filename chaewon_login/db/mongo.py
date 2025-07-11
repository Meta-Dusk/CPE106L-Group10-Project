from pymongo import MongoClient

MONGODB_CONNECTION_STRING = "localhost:27017" # Adjust if hosted remotely

def connect_to_mongo():
    try:
        client = MongoClient(f"mongodb://{MONGODB_CONNECTION_STRING}/", serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        db = client["ProjectATS"]
        print("Connected to MongoDB successfully.")
        return db["accounts"]
    except Exception as e:
        print("MongoDB connection failed:", e)
        return None

""" Run mongo.py to test database connection to MONGOD_CONNECTION_STRING """
def main():
    accounts_collection = connect_to_mongo()
    if accounts_collection is not None:
        print("Connected to MongoDB and 'accounts' collection is ready.")
    else:
        print("Failed to connect to MongoDB.")
        
if __name__ == "__main__":
    main()