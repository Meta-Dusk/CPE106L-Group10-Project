
from app.db.ride_data_manager import RideDataManager
from datetime import datetime
from typing import Dict, Optional

class RideBookingIntegration:
    """Helper class to integrate ride bookings with visualization system"""
    
    def __init__(self):
        self.data_manager = RideDataManager()
    
    def create_ride_booking(self, user_id: str, pickup_location: str, 
                          dropoff_location: str, **additional_data) -> Dict:
        """
        Call this when user creates a new ride booking
        Returns booking confirmation with ride_id
        """
        try:
            success = self.data_manager.save_ride_booking(
                user_id=user_id,
                pickup=pickup_location,
                dropoff=dropoff_location,
                **additional_data
            )
            
            if success:
                return {
                    "success": True,
                    "message": f"✅ Ride booked: {pickup_location} → {dropoff_location}",
                    "analytics_note": "This ride will appear in your analytics once completed."
                }
            else:
                return {
                    "success": False,
                    "message": "❌ Failed to book ride. Please try again."
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Booking error: {str(e)}"
            }
    
    def complete_ride(self, ride_id: str, wait_time_minutes: int, 
                     duration_minutes: int, fare_amount: float, 
                     driver_rating: int = None) -> Dict:
        """
        Call this when a ride is completed
        This is when the ride becomes available for analytics
        """
        try:
            success = self.data_manager.complete_ride(
                ride_id=ride_id,
                wait_time=wait_time_minutes,
                duration=duration_minutes,
                fare=fare_amount,
                driver_rating=driver_rating
            )
            
            if success:
                return {
                    "success": True,
                    "message": "✅ Ride completed! Added to your analytics.",
                    "analytics_ready": True
                }
            else:
                return {
                    "success": False,
                    "message": "❌ Failed to complete ride record."
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Completion error: {str(e)}"
            }
    
    def get_user_ride_summary(self, user_id: str) -> Dict:
        """Get a quick summary of user's ride data for dashboard display"""
        try:
            availability = self.data_manager.check_real_data_availability(user_id)
            stats = self.data_manager.get_ride_statistics(user_id)
            
            if "error" in stats:
                return {
                    "has_data": False,
                    "message": availability["message"],
                    "rides_count": availability["total_rides"],
                    "completed_count": availability["completed_rides"]
                }
            
            return {
                "has_data": True,
                "rides_count": stats["total_rides"],
                "completed_count": stats["completed_rides"],
                "total_spent": stats["fares"]["total"],
                "avg_wait_time": stats["wait_times"]["average"],
                "analytics_ready": availability["can_generate_charts"],
                "message": availability["message"]
            }
            
        except Exception as e:
            return {
                "has_data": False,
                "error": str(e),
                "message": "Error fetching ride summary"
            }


# Convenience functions for easy integration
ride_integration = RideBookingIntegration()

def book_ride(user_id: str, pickup: str, dropoff: str, **kwargs) -> Dict:
    """Simple function to book a ride - use this in your booking screen"""
    return ride_integration.create_ride_booking(user_id, pickup, dropoff, **kwargs)

def finish_ride(ride_id: str, wait_time: int, duration: int, fare: float, rating: int = None) -> Dict:
    """Simple function to complete a ride - use this when ride ends"""
    return ride_integration.complete_ride(ride_id, wait_time, duration, fare, rating)

def get_ride_summary(user_id: str) -> Dict:
    """Get user's ride summary for dashboard"""
    return ride_integration.get_user_ride_summary(user_id)
