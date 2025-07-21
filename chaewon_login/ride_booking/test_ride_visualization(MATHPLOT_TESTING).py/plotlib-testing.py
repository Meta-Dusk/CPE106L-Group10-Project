# test_ride_visualization.py

import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["chaewon_db"]
rides_collection = db["rides"]

# Insert sample rides
def insert_sample_rides(user_id):
    now = datetime.now()
    sample_rides = [
        {
            "user_id": user_id,
            "timestamp": (now - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "wait_time": 5 + i,
            "pickup": f"Location {i % 3 + 1}"
        }
        for i in range(10)
    ]
    rides_collection.insert_many(sample_rides)
    print(f"✅ Inserted {len(sample_rides)} sample rides for user '{user_id}'.")

# Matplotlib visualization
def visualize_user_rides(user_id):
    rides = list(rides_collection.find({"user_id": user_id}))
    if not rides:
        print("No rides found for user:", user_id)
        return

    timestamps = [r['timestamp'] for r in rides if 'timestamp' in r]
    wait_times = [r['wait_time'] for r in rides if 'wait_time' in r]
    locations = [r.get("pickup", "Unknown") for r in rides]

    # Frequency over time
    ride_days = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S").date() for t in timestamps]
    date_counts = {}
    for day in ride_days:
        date_counts[day] = date_counts.get(day, 0) + 1

    # Plot 1: Ride frequency
    plt.figure(figsize=(10, 4))
    plt.bar(date_counts.keys(), date_counts.values(), color='skyblue')
    plt.title("Ride Frequency Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Rides")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot 2: Wait times
    if wait_times:
        plt.figure(figsize=(6, 4))
        plt.hist(wait_times, bins=10, color='lightgreen', edgecolor='black')
        plt.title("Distribution of Wait Times")
        plt.xlabel("Minutes")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    # Plot 3: Pickup locations
    location_counts = {}
    for loc in locations:
        location_counts[loc] = location_counts.get(loc, 0) + 1
    plt.figure(figsize=(6, 4))
    plt.bar(location_counts.keys(), location_counts.values(), color='salmon')
    plt.title("Pickup Location Frequency")
    plt.xlabel("Location")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 🏁 Run everything
if __name__ == "__main__":
    test_user = "TMTmoney"
    insert_sample_rides(test_user)
    visualize_user_rides(test_user)
