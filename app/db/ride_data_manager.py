
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import sqlite3
from dotenv import load_dotenv
from typing import List, Dict, Optional
from app.db.sqlite import connect_to_sqlite, TABLE_NAME, DBKey

load_dotenv()

class RideDataManager:
    """Manages real ride data from actual app usage"""
    
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client["chaewon_db"]
        self.rides_collection = self.db["rides"]
        
        # SQLite connection for user data
        self.sqlite_conn = connect_to_sqlite()
    
    def get_user_rides(self, user_id: str) -> List[Dict]:
        """Fetch REAL rides for a specific user from actual app usage"""
        try:
            rides = list(self.rides_collection.find({"user_id": user_id}))
            print(f"📊 Found {len(rides)} real rides for user '{user_id}'")
            return rides
        except Exception as e:
            print(f"Error fetching rides: {e}")
            return []
    
    def save_ride_booking(self, user_id: str, pickup: str, dropoff: str, 
                         wait_time: int = None, duration: int = None, 
                         fare: float = None, **kwargs) -> bool:
        """Save a new ride booking from actual app usage"""
        try:
            ride_data = {
                "user_id": user_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "pickup": pickup,
                "dropoff": dropoff,
                "status": "requested",  # Can be: requested, confirmed, in_progress, completed, cancelled
                "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **kwargs  # Additional data like driver_id, vehicle_type, etc.
            }
            
            # Add optional fields if provided
            if wait_time is not None:
                ride_data["wait_time"] = wait_time
            if duration is not None:
                ride_data["duration"] = duration  
            if fare is not None:
                ride_data["fare"] = fare
                
            result = self.rides_collection.insert_one(ride_data)
            print(f"✅ Saved new ride booking for '{user_id}': {pickup} → {dropoff}")
            return bool(result.inserted_id)
            
        except Exception as e:
            print(f"❌ Error saving ride booking: {e}")
            return False
    
    def update_ride_status(self, ride_id: str, status: str, **updates) -> bool:
        """Update ride status and other fields (for when ride is completed)"""
        try:
            update_data = {
                "status": status,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **updates
            }
            
            result = self.rides_collection.update_one(
                {"_id": ride_id}, 
                {"$set": update_data}
            )
            print(f"✅ Updated ride {ride_id} status to '{status}'")
            return result.modified_count > 0
            
        except Exception as e:
            print(f"❌ Error updating ride: {e}")
            return False
    
    def complete_ride(self, ride_id: str, wait_time: int, duration: int, 
                     fare: float, driver_rating: int = None, **kwargs) -> bool:
        """Mark ride as completed with final details"""
        completion_data = {
            "status": "completed",
            "wait_time": wait_time,
            "duration": duration, 
            "fare": fare,
            "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if driver_rating:
            completion_data["driver_rating"] = driver_rating
            
        completion_data.update(kwargs)  # Additional completion data
        
        return self.update_ride_status(ride_id, "completed", **completion_data)
    
    def get_ride_statistics(self, user_id: str) -> Dict:
        """Get comprehensive ride statistics from REAL data only"""
        rides = self.get_user_rides(user_id)
        
        if not rides:
            return {
                "error": "No real ride data found",
                "message": "User hasn't booked any rides yet. Statistics will appear after actual app usage."
            }
        
        # Only process completed rides for accurate statistics
        completed_rides = [r for r in rides if r.get('status') == 'completed']
        
        if not completed_rides:
            return {
                "error": "No completed rides found", 
                "message": f"Found {len(rides)} ride(s) but none are completed yet.",
                "pending_rides": len(rides)
            }
        
        # Calculate statistics from real data
        wait_times = [r.get('wait_time', 0) for r in completed_rides if r.get('wait_time')]
        durations = [r.get('duration', 0) for r in completed_rides if r.get('duration')]
        fares = [r.get('fare', 0) for r in completed_rides if r.get('fare')]
        
        # Count pickup locations from real rides
        pickup_counts = {}
        for ride in completed_rides:
            pickup = ride.get('pickup', 'Unknown')
            pickup_counts[pickup] = pickup_counts.get(pickup, 0) + 1
        
        # Calculate date range from real timestamps
        timestamps = []
        for ride in completed_rides:
            try:
                ts = datetime.strptime(ride['timestamp'], "%Y-%m-%d %H:%M:%S")
                timestamps.append(ts)
            except (KeyError, ValueError):
                continue
        
        return {
            "total_rides": len(rides),
            "completed_rides": len(completed_rides),
            "date_range": {
                "start": min(timestamps).date() if timestamps else None,
                "end": max(timestamps).date() if timestamps else None
            },
            "wait_times": {
                "average": sum(wait_times) / len(wait_times) if wait_times else 0,
                "median": sorted(wait_times)[len(wait_times)//2] if wait_times else 0,
                "min": min(wait_times) if wait_times else 0,
                "max": max(wait_times) if wait_times else 0,
                "data": wait_times,
                "count": len(wait_times)
            },
            "durations": {
                "average": sum(durations) / len(durations) if durations else 0,
                "data": durations,
                "count": len(durations)
            },
            "fares": {
                "average": sum(fares) / len(fares) if fares else 0,
                "total": sum(fares),
                "data": fares,
                "count": len(fares)
            },
            "locations": {
                "total_served": len(pickup_counts),
                "pickup_counts": pickup_counts,
                "most_popular": max(pickup_counts.items(), key=lambda x: x[1]) if pickup_counts else None
            },
            "data_source": "real_usage"
        }
    
    def get_user_info(self, user_id: str) -> Dict:
        """Get user information from SQLite"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE {DBKey.USERNAME.value} = ?", (user_id,))
            user = cursor.fetchone()
            
            if user:
                return {
                    "username": user[DBKey.USERNAME.value],
                    "is_admin": bool(user[DBKey.OP.value]),
                    "exists": True
                }
            else:
                return {"exists": False, "message": f"User '{user_id}' not found"}
                
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return {"exists": False, "error": str(e)}
    
    def get_all_users_with_rides(self) -> List[str]:
        """Get list of all users who have ride data"""
        try:
            users = self.rides_collection.distinct("user_id")
            return users
        except Exception as e:
            print(f"Error getting users with rides: {e}")
            return []
    
    def check_real_data_availability(self, user_id: str) -> Dict:
        """Check if user has real ride data available for visualization"""
        rides = self.get_user_rides(user_id)
        completed_rides = [r for r in rides if r.get('status') == 'completed']
        
        return {
            "has_data": len(completed_rides) > 0,
            "total_rides": len(rides),
            "completed_rides": len(completed_rides),
            "can_generate_charts": len(completed_rides) >= 3,  # Minimum for meaningful charts
            "message": self._get_data_availability_message(len(rides), len(completed_rides))
        }
    
    def _get_data_availability_message(self, total: int, completed: int) -> str:
        """Generate user-friendly message about data availability"""
        if completed >= 10:
            return f"Great! You have {completed} completed rides. Rich analytics available!"
        elif completed >= 3:
            return f"You have {completed} completed rides. Basic analytics available."
        elif completed > 0:
            return f"You have {completed} completed ride(s). More rides needed for detailed analytics."
        elif total > 0:
            return f"You have {total} pending/in-progress ride(s). Complete them to see analytics."
        else:
            return "No rides found. Start booking rides to see your personal analytics!"

    # Keep for backward compatibility but mark as deprecated
    def ensure_data_exists(self, user_id: str) -> bool:
        """
        DEPRECATED: Check if user has real data, no longer creates sample data
        Use check_real_data_availability() instead
        """
        print("⚠️ Warning: ensure_data_exists() is deprecated. App now uses real data only.")
        availability = self.check_real_data_availability(user_id)
        return availability["has_data"]
