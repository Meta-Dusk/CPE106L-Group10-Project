from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["chaewon_db"]
rides = db["rides"]

sample_ride = {
    "user_id": "TMTmoney",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "wait_time": 7,
    "pickup": "Ayala"
}

rides.insert_one(sample_ride)
print("✅ Inserted sample ride for TMTmoney")
