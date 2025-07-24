"""
Ride Data Visualization Screen
Flet UI Integration for Ride Visualization with Matplotlib Charts
"""

import flet as ft
import base64
from io import BytesIO
from typing import Dict, Optional
from app.services.visualization_service import RideVisualizationService
from app.ui.components.containers import default_container
from app.ui.components.buttons import default_action_button
from app.ui.components.text import default_text
from app.ui.styles import DefaultTextStyle

class RideVisualizationUI:
    """Flet UI integration for ride visualizations"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.service = RideVisualizationService()
        # Get current user from session (Flet session syntax)
        self.current_user = page.session.get("user_id")
        if not self.current_user:
            # If no user in session, redirect to login
            page.go("/")
            return
    
    def create_visualization_container(self, chart_data: bytes, title: str, description: str) -> ft.Container:
        """Create a container with embedded matplotlib chart"""
        # Convert bytes to base64 for display
        chart_base64 = base64.b64encode(chart_data).decode()
        
        return default_container(
            ft.Column(
                controls=[
                    default_text(DefaultTextStyle.TITLE, title),
                    default_text(DefaultTextStyle.SUBTITLE, description),
                    ft.Image(
                        src_base64=chart_base64,
                        width=800,
                        height=600,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=ft.border_radius.all(8),
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    
    def create_analysis_controls(self) -> ft.Container:
        """Create control panel for analysis options"""
        
        def on_frequency_click(e):
            self.show_frequency_analysis()
        
        def on_wait_time_click(e):
            self.show_wait_time_analysis()
        
        def on_coverage_click(e):
            self.show_coverage_analysis()
        
        def on_dashboard_click(e):
            self.show_comprehensive_dashboard()
        
        def on_refresh_data_click(e):
            self.refresh_data()
        
        controls_row = ft.Row(
            controls=[
                default_action_button(
                    text="📈 Frequency",
                    on_click=on_frequency_click
                ),
                default_action_button(
                    text="⏱️ Wait Times", 
                    on_click=on_wait_time_click
                ),
                default_action_button(
                    text="🗺️ Coverage",
                    on_click=on_coverage_click
                ),
                default_action_button(
                    text="📋 Dashboard",
                    on_click=on_dashboard_click
                ),
                default_action_button(
                    text="🔄 Refresh",
                    on_click=on_refresh_data_click
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        
        return default_container(
            ft.Column(
                controls=[
                    default_text(DefaultTextStyle.TITLE, "Ride Data Analysis"),
                    default_text(DefaultTextStyle.SUBTITLE, f"Analysis for user: {self.current_user}"),
                    controls_row,
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    
    def show_frequency_analysis(self):
        """Display ride frequency analysis"""
        try:
            result = self.service.generate_frequency_analysis(
                self.current_user, 
                show_plot=False
            )
            
            if "error" in result:
                self.show_error_dialog(result["error"])
                return
            
            # Get chart bytes from service
            chart_bytes = self.service.frequency_chart.get_chart_bytes()
            
            # Create visualization container
            chart_container = self.create_visualization_container(
                chart_bytes,
                "📈 Ride Frequency Analysis",
                f"Ride patterns over time for {self.current_user}"
            )
            
            # Update page content
            self.update_content_area(chart_container)
            
        except Exception as e:
            self.show_error_dialog(f"Error generating frequency analysis: {e}")
    
    def show_wait_time_analysis(self):
        """Display wait time distribution analysis"""
        try:
            result = self.service.generate_wait_time_analysis(
                self.current_user, 
                show_plot=False
            )
            
            if "error" in result:
                self.show_error_dialog(result["error"])
                return
            
            # Get chart bytes from service
            chart_bytes = self.service.wait_time_chart.get_chart_bytes()
            
            # Create visualization container
            chart_container = self.create_visualization_container(
                chart_bytes,
                "⏱️ Wait Time Distribution",
                f"Wait time patterns for {self.current_user}"
            )
            
            # Update page content
            self.update_content_area(chart_container)
            
        except Exception as e:
            self.show_error_dialog(f"Error generating wait time analysis: {e}")
    
    def show_coverage_analysis(self):
        """Display service coverage analysis"""
        try:
            result = self.service.generate_coverage_analysis(
                self.current_user, 
                show_plot=False
            )
            
            if "error" in result:
                self.show_error_dialog(result["error"])
                return
            
            # Get chart bytes from service
            chart_bytes = self.service.coverage_chart.get_chart_bytes()
            
            # Create visualization container
            chart_container = self.create_visualization_container(
                chart_bytes,
                "🗺️ Service Coverage Analysis",
                f"Location coverage for {self.current_user}"
            )
            
            # Update page content
            self.update_content_area(chart_container)
            
        except Exception as e:
            self.show_error_dialog(f"Error generating coverage analysis: {e}")
    
    def show_comprehensive_dashboard(self):
        """Display comprehensive dashboard"""
        try:
            result = self.service.generate_comprehensive_dashboard(
                self.current_user, 
                show_plot=False
            )
            
            if "error" in result:
                self.show_error_dialog(result["error"])
                return
            
            # Get dashboard bytes from service
            chart_bytes = self.service.dashboard.get_chart_bytes()
            
            # Create visualization container
            chart_container = self.create_visualization_container(
                chart_bytes,
                "📋 Comprehensive Dashboard",
                f"Complete ride analysis for {self.current_user}"
            )
            
            # Update page content
            self.update_content_area(chart_container)
            
        except Exception as e:
            self.show_error_dialog(f"Error generating dashboard: {e}")
    
    def refresh_data(self):
        """Refresh charts with latest real data"""
        try:
            # Clear current chart to force refresh
            self.chart_container.content = ft.Column([
                ft.Icon(ft.Icons.REFRESH, size=100, color=ft.Colors.PRIMARY),
                ft.Text("Charts Refreshed", size=24, text_align=ft.TextAlign.CENTER),
                ft.Text("Use the buttons above to view updated analytics", size=16, text_align=ft.TextAlign.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            self.page.update()
            
            # Show success dialog
            def close_dialog(e):
                dialog.open = False
                self.page.update()
            
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("✅ Data Refreshed"),
                content=ft.Text("Sample data has been refreshed successfully."),
                actions=[
                    ft.TextButton("OK", on_click=close_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()
            
        except Exception as e:
            self.show_error_dialog(f"Error refreshing data: {e}")
    
    def show_error_dialog(self, error_message: str):
        """Show error dialog"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("❌ Error"),
            content=ft.Text(error_message),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def update_content_area(self, new_content: ft.Control):
        """Update the main content area with new visualization"""
        # Clear existing content (assuming content area is at index 1)
        if len(self.page.controls) > 1:
            self.page.controls[1] = new_content
        else:
            self.page.controls.append(new_content)
        
        self.page.update()
    
    def create_main_view(self) -> ft.Column:
        """Create the main visualization view"""
        
        # Control panel
        controls = self.create_analysis_controls()
        
        # Initial welcome content
        welcome_content = default_container(
            ft.Column(
                controls=[
                    default_text(DefaultTextStyle.TITLE, "🚗 Ride Data Visualization"),
                    default_text(DefaultTextStyle.SUBTITLE, "Select an analysis type to view charts"),
                    ft.Icon(
                        ft.Icons.ANALYTICS,
                        size=100,
                        color=ft.Colors.BLUE_300,
                    ),
                    ft.Text(
                        "Use the buttons above to generate different types of ride analysis charts.",
                        text_align=ft.TextAlign.CENTER,
                        size=16,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        
        return ft.Column(
            controls=[
                controls,
                welcome_content,
            ],
            spacing=20,
            expand=True,
        )


# Builder and utility functions
class VisualizationPageBuilder:
    """Builder for creating visualization page"""
    
    @staticmethod
    def build_page(page: ft.Page) -> ft.Column:
        """Build complete visualization page"""
        
        # Configure page
        page.title = "Ride Data Visualization"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.window_width = 1200
        page.window_height = 800
        
        # Create UI manager
        viz_ui = RideVisualizationUI(page)
        
        # Return main view
        return viz_ui.create_main_view()


def create_visualization_page(page: ft.Page) -> ft.Column:
    """Create a complete ride visualization page"""
    return VisualizationPageBuilder.build_page(page)