# ride_list.py
import flet as ft
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["chaewon_db"]
rides_collection = db["rides"]

def ride_list_view(user_id="TMTmoney"):
    # Get user rides from DB
    rides = list(rides_collection.find({"user_id": user_id}))

    if not rides:
        return ft.Column([ft.Text("No rides found.")])

    ride_widgets = []
    for ride in rides:
        ride_widgets.append(
            ft.Card(
                content=ft.ListTile(
                    title=ft.Text(f"Ride at {ride.get('timestamp', 'No time')}"),
                    subtitle=ft.Text(
                        f"From: {ride.get('pickup', 'N/A')} → {ride.get('dropoff', 'N/A')}\n"
                        f"Wait Time: {ride.get('wait_time', '?')} min"
                    )
                )
            )
        )
    
    return ft.Column(ride_widgets)
