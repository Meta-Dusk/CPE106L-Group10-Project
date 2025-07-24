
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import tempfile
import os

class BaseVisualizationComponent:
    """Base class for all visualization components"""
    
    def __init__(self, title: str = "", figsize: Tuple[int, int] = (10, 6)):
        self.title = title
        self.figsize = figsize
        self.fig = None
        self.ax = None
    
    def setup_plot(self, title_override: str = None):
        """Setup basic plot configuration"""
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        plt.title(title_override or self.title, fontsize=16, fontweight='bold')
        plt.grid(alpha=0.3)
    
    def save_plot(self, filename: str = None) -> str:
        """Save plot to temporary file and return path"""
        if not filename:
            filename = tempfile.mktemp(suffix='.png')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        return filename
    
    def show_plot(self):
        """Display the plot"""
        plt.tight_layout()
        plt.show()
    
    def close_plot(self):
        """Close the plot to free memory"""
        if self.fig:
            plt.close(self.fig)
    
    def get_chart_bytes(self) -> bytes:
        """Get chart as bytes for UI integration"""
        from io import BytesIO
        buffer = BytesIO()
        if self.fig:
            self.fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            return buffer.getvalue()
        return b''


class RideFrequencyChart(BaseVisualizationComponent):
    """Component for ride frequency over time visualization"""
    
    def __init__(self):
        super().__init__("📊 Ride Frequency Over Time", (12, 6))
    
    def create_chart(self, rides_data: List[Dict], user_id: str) -> Dict:
        """Create ride frequency chart"""
        if not rides_data:
            return {"error": "No rides data provided"}
        
        # Parse timestamps and group by date
        timestamps = [datetime.strptime(r['timestamp'], "%Y-%m-%d %H:%M:%S") for r in rides_data]
        ride_dates = [t.date() for t in timestamps]
        
        # Count rides per day
        date_counts = {}
        for date in ride_dates:
            date_counts[date] = date_counts.get(date, 0) + 1
        
        # Sort dates
        sorted_dates = sorted(date_counts.keys())
        counts = [date_counts[date] for date in sorted_dates]
        
        # Create the plot
        self.setup_plot(f'📊 Ride Frequency Over Time for {user_id}')
        
        bars = self.ax.bar(sorted_dates, counts, color='skyblue', alpha=0.7, edgecolor='navy')
        self.ax.set_xlabel('Date', fontsize=12)
        self.ax.set_ylabel('Number of Rides', fontsize=12)
        self.ax.tick_params(axis='x', rotation=45)
        
        # Add average line
        avg_rides = np.mean(counts)
        self.ax.axhline(y=avg_rides, color='red', linestyle='--', 
                       label=f'Average: {avg_rides:.1f} rides/day')
        self.ax.legend()
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            self.ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(count), ha='center', va='bottom', fontweight='bold')
        
        return {
            "total_rides": len(rides_data),
            "date_range": f"{min(sorted_dates)} to {max(sorted_dates)}",
            "average_per_day": avg_rides,
            "chart_data": {
                "dates": sorted_dates,
                "counts": counts
            }
        }


class WaitTimeDistributionChart(BaseVisualizationComponent):
    """Component for wait time distribution visualization"""
    
    def __init__(self):
        super().__init__("⏱️ Wait Time Distribution", (10, 6))
    
    def create_chart(self, rides_data: List[Dict], user_id: str) -> Dict:
        """Create wait time distribution chart"""
        wait_times = [r.get('wait_time', 0) for r in rides_data if 'wait_time' in r]
        
        if not wait_times:
            return {"error": "No wait time data available"}
        
        # Create histogram
        self.setup_plot(f'⏱️ Wait Time Distribution for {user_id}')
        
        n, bins, patches = self.ax.hist(wait_times, bins=15, color='lightgreen', 
                                       edgecolor='darkgreen', alpha=0.7)
        
        self.ax.set_xlabel('Wait Time (minutes)', fontsize=12)
        self.ax.set_ylabel('Frequency', fontsize=12)
        
        # Add statistics
        avg_wait = np.mean(wait_times)
        median_wait = np.median(wait_times)
        
        self.ax.axvline(avg_wait, color='red', linestyle='--', linewidth=2, 
                       label=f'Average: {avg_wait:.1f} min')
        self.ax.axvline(median_wait, color='orange', linestyle='--', linewidth=2, 
                       label=f'Median: {median_wait:.1f} min')
        
        self.ax.legend()
        
        return {
            "statistics": {
                "average": avg_wait,
                "median": median_wait,
                "min": min(wait_times),
                "max": max(wait_times),
                "total_samples": len(wait_times)
            },
            "distribution_data": {
                "bins": bins.tolist(),
                "counts": n.tolist()
            }
        }


class ServiceCoverageChart(BaseVisualizationComponent):
    """Component for service coverage visualization"""
    
    def __init__(self):
        super().__init__("🗺️ Service Coverage", (12, 8))
    
    def create_chart(self, rides_data: List[Dict], user_id: str, top_n: int = 10) -> Dict:
        """Create service coverage chart"""
        # Count pickup locations
        pickup_counts = {}
        for ride in rides_data:
            pickup = ride.get('pickup', 'Unknown')
            pickup_counts[pickup] = pickup_counts.get(pickup, 0) + 1
        
        if not pickup_counts:
            return {"error": "No pickup location data available"}
        
        # Sort by frequency and take top N
        sorted_locations = sorted(pickup_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        locations = [item[0] for item in sorted_locations]
        counts = [item[1] for item in sorted_locations]
        
        # Create horizontal bar chart
        self.setup_plot(f'🗺️ Service Coverage - Top {len(locations)} Pickup Locations for {user_id}')
        
        bars = self.ax.barh(locations, counts, color='salmon', alpha=0.7, edgecolor='darkred')
        self.ax.set_xlabel('Number of Rides', fontsize=12)
        self.ax.set_ylabel('Pickup Location', fontsize=12)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            self.ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                        str(count), ha='left', va='center', fontweight='bold')
        
        return {
            "total_locations": len(pickup_counts),
            "top_locations": dict(sorted_locations),
            "most_popular": sorted_locations[0] if sorted_locations else None,
            "coverage_data": {
                "locations": locations,
                "counts": counts
            }
        }


class ComprehensiveDashboard(BaseVisualizationComponent):
    """Component for comprehensive dashboard with multiple charts"""
    
    def __init__(self):
        super().__init__("🚗 ATS Ride Analytics Dashboard", (16, 12))
    
    def create_dashboard(self, rides_data: List[Dict], user_id: str) -> Dict:
        """Create comprehensive dashboard"""
        if not rides_data:
            return {"error": "No rides data provided"}
        
        # Create a 2x2 subplot dashboard
        self.fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=self.figsize)
        self.fig.suptitle(f'🚗 ATS Ride Analytics Dashboard for {user_id}', 
                         fontsize=18, fontweight='bold')
        
        # 1. Ride frequency over time
        timestamps = [datetime.strptime(r['timestamp'], "%Y-%m-%d %H:%M:%S") for r in rides_data]
        ride_dates = [t.date() for t in timestamps]
        date_counts = {}
        for date in ride_dates:
            date_counts[date] = date_counts.get(date, 0) + 1
        
        sorted_dates = sorted(date_counts.keys())
        counts = [date_counts[date] for date in sorted_dates]
        
        ax1.bar(sorted_dates, counts, color='skyblue', alpha=0.7)
        ax1.set_title('📊 Ride Frequency Over Time')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Number of Rides')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Wait time distribution
        wait_times = [r.get('wait_time', 0) for r in rides_data if 'wait_time' in r]
        ax2.hist(wait_times, bins=10, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
        ax2.set_title('⏱️ Wait Time Distribution')
        ax2.set_xlabel('Wait Time (minutes)')
        ax2.set_ylabel('Frequency')
        if wait_times:
            ax2.axvline(np.mean(wait_times), color='red', linestyle='--', 
                       label=f'Avg: {np.mean(wait_times):.1f} min')
            ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Service coverage (top 8 locations)
        pickup_counts = {}
        for ride in rides_data:
            pickup = ride.get('pickup', 'Unknown')
            pickup_counts[pickup] = pickup_counts.get(pickup, 0) + 1
        
        sorted_locations = sorted(pickup_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        locations = [item[0] for item in sorted_locations]
        pickup_freq = [item[1] for item in sorted_locations]
        
        ax3.barh(locations, pickup_freq, color='salmon', alpha=0.7)
        ax3.set_title('🗺️ Top Service Areas')
        ax3.set_xlabel('Number of Rides')
        ax3.grid(axis='x', alpha=0.3)
        
        # 4. Ride duration vs fare analysis
        durations = [r.get('duration', 0) for r in rides_data if 'duration' in r]
        fares = [r.get('fare', 0) for r in rides_data if 'fare' in r]
        
        if durations and fares:
            ax4.scatter(durations, fares, alpha=0.6, color='purple', s=50)
            ax4.set_title('💰 Duration vs Fare Analysis')
            ax4.set_xlabel('Ride Duration (minutes)')
            ax4.set_ylabel('Fare (₱)')
            ax4.grid(alpha=0.3)
            
            # Add trend line
            if len(durations) > 1:
                z = np.polyfit(durations, fares, 1)
                p = np.poly1d(z)
                ax4.plot(durations, p(durations), "r--", alpha=0.8, linewidth=2)
        
        return {
            "dashboard_created": True,
            "summary": {
                "total_rides": len(rides_data),
                "avg_wait_time": np.mean(wait_times) if wait_times else 0,
                "service_locations": len(pickup_counts),
                "avg_fare": np.mean(fares) if fares else 0,
                "avg_duration": np.mean(durations) if durations else 0
            }
        }
