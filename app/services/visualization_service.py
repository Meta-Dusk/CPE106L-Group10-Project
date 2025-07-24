
from typing import Dict, List, Optional
from app.db.ride_data_manager import RideDataManager
from app.ui.components.visualization_components import (
    RideFrequencyChart,
    WaitTimeDistributionChart, 
    ServiceCoverageChart,
    ComprehensiveDashboard
)

class RideVisualizationService:
    """Service layer for ride data visualization"""
    
    def __init__(self):
        self.data_manager = RideDataManager()
        self.frequency_chart = RideFrequencyChart()
        self.wait_time_chart = WaitTimeDistributionChart()
        self.coverage_chart = ServiceCoverageChart()
        self.dashboard = ComprehensiveDashboard()
    
    def generate_frequency_analysis(self, user_id: str, show_plot: bool = True, save_path: str = None) -> Dict:
        """Generate ride frequency analysis from REAL user data"""
        try:
            # Check if user has real data available
            availability = self.data_manager.check_real_data_availability(user_id)
            
            if not availability["can_generate_charts"]:
                return {
                    "error": "Insufficient real data for visualization",
                    "message": availability["message"],
                    "total_rides": availability["total_rides"],
                    "completed_rides": availability["completed_rides"],
                    "data_source": "real_usage"
                }
            
            # Get real ride data
            rides_data = self.data_manager.get_user_rides(user_id)
            if not rides_data:
                return {
                    "error": f"No ride data found for user {user_id}",
                    "message": "Start booking rides to see your analytics!",
                    "data_source": "real_usage"
                }
            
            # Create chart from real data
            result = self.frequency_chart.create_chart(rides_data, user_id)
            
            # Handle display/save
            if save_path:
                saved_path = self.frequency_chart.save_plot(save_path)
                result["saved_to"] = saved_path
            
            if show_plot:
                self.frequency_chart.show_plot()
            
            self.frequency_chart.close_plot()
            
            print(f"📈 Frequency Analysis for {user_id}:")
            print(f"   Total rides: {result.get('total_rides', 0)}")
            print(f"   Data source: Real user activity")
            
            return result
            
        except Exception as e:
            error_msg = f"Error generating frequency analysis: {e}"
            print(error_msg)
            return {"error": error_msg, "data_source": "real_usage"}
    
    def generate_wait_time_analysis(self, user_id: str, show_plot: bool = True, save_path: str = None) -> Dict:
        """Generate wait time distribution analysis"""
        try:
            # Check if real data is available
            if not self.data_manager.check_real_data_availability(user_id):
                return {"error": "No completed rides yet. Start booking and completing rides to see your wait time patterns!"}
            
            # Get data
            rides_data = self.data_manager.get_user_rides(user_id)
            if not rides_data:
                return {"error": "No ride data found. Complete some rides to see wait time analysis."}
            
            # Create chart
            result = self.wait_time_chart.create_chart(rides_data, user_id)
            
            # Handle display/save
            if save_path:
                saved_path = self.wait_time_chart.save_plot(save_path)
                result["saved_to"] = saved_path
            
            if show_plot:
                self.wait_time_chart.show_plot()
            
            self.wait_time_chart.close_plot()
            
            stats = result.get('statistics', {})
            print(f"⏱️ Wait Time Analysis for {user_id}:")
            print(f"   Average: {stats.get('average', 0):.1f} minutes")
            print(f"   Median: {stats.get('median', 0):.1f} minutes")
            print(f"   Range: {stats.get('min', 0)}-{stats.get('max', 0)} minutes")
            
            return result
            
        except Exception as e:
            error_msg = f"Error generating wait time analysis: {e}"
            print(error_msg)
            return {"error": error_msg}
    
    def generate_coverage_analysis(self, user_id: str, top_n: int = 10, show_plot: bool = True, save_path: str = None) -> Dict:
        """Generate service coverage analysis"""
        try:
            # Check if real data is available
            if not self.data_manager.check_real_data_availability(user_id):
                return {"error": "No completed rides yet. Start booking and completing rides to see your service coverage!"}
            
            # Get data
            rides_data = self.data_manager.get_user_rides(user_id)
            if not rides_data:
                return {"error": "No ride data found. Complete some rides to see coverage analysis."}
            
            # Create chart
            result = self.coverage_chart.create_chart(rides_data, user_id, top_n)
            
            # Handle display/save
            if save_path:
                saved_path = self.coverage_chart.save_plot(save_path)
                result["saved_to"] = saved_path
            
            if show_plot:
                self.coverage_chart.show_plot()
            
            self.coverage_chart.close_plot()
            
            print(f"🗺️ Service Coverage Analysis for {user_id}:")
            print(f"   Total locations served: {result.get('total_locations', 0)}")
            if result.get('most_popular'):
                location, count = result['most_popular']
                print(f"   Most popular: {location} ({count} rides)")
            
            return result
            
        except Exception as e:
            error_msg = f"Error generating coverage analysis: {e}"
            print(error_msg)
            return {"error": error_msg}
    
    def generate_comprehensive_dashboard(self, user_id: str, show_plot: bool = True, save_path: str = None) -> Dict:
        """Generate comprehensive dashboard with all visualizations"""
        try:
            # Check if real data is available
            if not self.data_manager.check_real_data_availability(user_id):
                return {"error": "No completed rides yet. Start booking and completing rides to see your comprehensive dashboard!"}
            
            # Get data
            rides_data = self.data_manager.get_user_rides(user_id)
            if not rides_data:
                return {"error": "No ride data found. Complete some rides to see your dashboard."}
            
            # Create dashboard
            result = self.dashboard.create_dashboard(rides_data, user_id)
            
            # Handle display/save
            if save_path:
                saved_path = self.dashboard.save_plot(save_path)
                result["saved_to"] = saved_path
            
            if show_plot:
                self.dashboard.show_plot()
            
            self.dashboard.close_plot()
            
            summary = result.get('summary', {})
            print(f"📋 Comprehensive Dashboard for {user_id}:")
            print(f"   Total rides: {summary.get('total_rides', 0)}")
            print(f"   Average wait time: {summary.get('avg_wait_time', 0):.1f} minutes")
            print(f"   Service locations: {summary.get('service_locations', 0)}")
            print(f"   Average fare: ₱{summary.get('avg_fare', 0):.0f}")
            print(f"   Average duration: {summary.get('avg_duration', 0):.0f} minutes")
            
            return result
            
        except Exception as e:
            error_msg = f"Error generating dashboard: {e}"
            print(error_msg)
            return {"error": error_msg}
    
    def get_user_statistics(self, user_id: str) -> Dict:
        """Get comprehensive user statistics without generating plots"""
        try:
            return self.data_manager.get_ride_statistics(user_id)
        except Exception as e:
            return {"error": f"Error getting user statistics: {e}"}
    
    def run_complete_analysis(self, user_id: str = "TMTmoney", save_charts: bool = False) -> Dict:
        """Run complete ride data analysis with all visualizations"""
        print(f"🚀 Starting Complete Ride Data Analysis for {user_id}")
        print("=" * 60)
        
        results = {
            "user_id": user_id,
            "analysis_complete": False,
            "errors": []
        }
        
        try:
            # 1. Frequency Analysis
            print("\n1️⃣ Generating Ride Frequency Analysis...")
            freq_result = self.generate_frequency_analysis(user_id, show_plot=True)
            if "error" in freq_result:
                results["errors"].append(f"Frequency analysis: {freq_result['error']}")
            else:
                results["frequency_analysis"] = freq_result
            
            # 2. Wait Time Analysis
            print("\n2️⃣ Generating Wait Time Analysis...")
            wait_result = self.generate_wait_time_analysis(user_id, show_plot=True)
            if "error" in wait_result:
                results["errors"].append(f"Wait time analysis: {wait_result['error']}")
            else:
                results["wait_time_analysis"] = wait_result
            
            # 3. Coverage Analysis
            print("\n3️⃣ Generating Service Coverage Analysis...")
            coverage_result = self.generate_coverage_analysis(user_id, show_plot=True)
            if "error" in coverage_result:
                results["errors"].append(f"Coverage analysis: {coverage_result['error']}")
            else:
                results["coverage_analysis"] = coverage_result
            
            # 4. Comprehensive Dashboard
            print("\n4️⃣ Generating Comprehensive Dashboard...")
            dashboard_result = self.generate_comprehensive_dashboard(user_id, show_plot=True)
            if "error" in dashboard_result:
                results["errors"].append(f"Dashboard: {dashboard_result['error']}")
            else:
                results["dashboard"] = dashboard_result
            
            # Summary
            if not results["errors"]:
                results["analysis_complete"] = True
                print("\n✅ Complete analysis finished!")
                print("📊 All matplotlib visualizations generated successfully")
            else:
                print(f"\n⚠️ Analysis completed with {len(results['errors'])} errors")
                for error in results["errors"]:
                    print(f"   - {error}")
            
            return results
            
        except Exception as e:
            error_msg = f"Critical error in complete analysis: {e}"
            print(error_msg)
            results["errors"].append(error_msg)
            return results
