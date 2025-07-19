# ride_visuals_utils.py

import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["chaewon_db"]
rides_collection = db["rides"]

def visualize_user_rides(user_id):
    rides = list(rides_collection.find({"user_id": user_id}))
    if not rides:
        print("No rides found for user:", user_id)
        return

    timestamps = [r['timestamp'] for r in rides if 'timestamp' in r]
    wait_times = [r['wait_time'] for r in rides if 'wait_time' in r]
    locations = [r.get("pickup", "Unknown") for r in rides]

    ride_days = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S").date() for t in timestamps]
    date_counts = {}
    for day in ride_days:
        date_counts[day] = date_counts.get(day, 0) + 1

    plt.figure(figsize=(10, 4))
    plt.bar(date_counts.keys(), date_counts.values(), color='skyblue')
    plt.title("Ride Frequency Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Rides")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    if wait_times:
        plt.figure(figsize=(6, 4))
        plt.hist(wait_times, bins=10, color='lightgreen', edgecolor='black')
        plt.title("Distribution of Wait Times")
        plt.xlabel("Minutes")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

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
