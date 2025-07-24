import flet as ft
import base64

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import div, default_row
from app.ui.screens.shared_ui import render_page, preset_logout_button, open_profile, theme_toggle_button, mod_toggle_theme
from app.ui.animations import container_setup
from app.assets.images import set_logo
from app.routing.route_data import PageRoute
from app.services.visualization_service import RideVisualizationService

def handle_viewgraphs(page: ft.Page, _):
    logo = set_logo()
    
    # Initialize visualization service
    viz_service = RideVisualizationService()
    
    # Get current user from session (Flet session syntax)
    current_user = page.session.get("user_id")
    if not current_user:
        # If no user in session, redirect to login
        page.go("/")
        return
    
    # Create a reference for the chart container
    chart_container_ref = ft.Ref[ft.Container]()
    
    def create_chart_image_from_bytes(chart_bytes: bytes, title: str) -> ft.Column:
        """Convert chart bytes to displayable image"""
        if len(chart_bytes) == 0:
            return ft.Column([
                ft.Text("No chart data available", size=16, color=ft.Colors.ERROR),
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.ERROR, size=48)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        chart_base64 = base64.b64encode(chart_bytes).decode()
        return ft.Column([
            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Image(
                src_base64=chart_base64,
                width=700,
                height=400,
                fit=ft.ImageFit.CONTAIN,
                border_radius=ft.border_radius.all(8),
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    def show_frequency_chart(e):
        """Show ride frequency analysis chart"""
        try:
            result = viz_service.generate_frequency_analysis(current_user, show_plot=False)
            if "error" in result:
                chart_container_ref.current.content = ft.Column([
                    ft.Icon(ft.Icons.ANALYTICS, size=100, color=ft.Colors.OUTLINE),
                    ft.Text("📊 Ride Frequency Analysis", size=24, text_align=ft.TextAlign.CENTER),
                    ft.Text(result["error"], size=16, text_align=ft.TextAlign.CENTER, color=ft.Colors.OUTLINE),
                    ft.ElevatedButton(
                        "Start Booking Rides",
                        icon=ft.Icons.ADD_LOCATION,
                        on_click=lambda _: page.go("/dashboard"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PRIMARY,
                            color=ft.Colors.ON_PRIMARY
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            else:
                chart_bytes = viz_service.frequency_chart.get_chart_bytes()
                chart_image = create_chart_image_from_bytes(chart_bytes, "📈 Ride Frequency Analysis")
                chart_container_ref.current.content = chart_image
            page.update()
        except Exception as ex:
            show_error_dialog(f"Failed to generate frequency chart: {str(ex)}")
    
    def show_wait_time_chart(e):
        """Show wait time distribution chart"""
        try:
            result = viz_service.generate_wait_time_analysis(current_user, show_plot=False)
            if "error" in result:
                chart_container_ref.current.content = ft.Column([
                    ft.Icon(ft.Icons.TIMER, size=100, color=ft.Colors.OUTLINE),
                    ft.Text("⏱️ Wait Time Distribution", size=24, text_align=ft.TextAlign.CENTER),
                    ft.Text(result["error"], size=16, text_align=ft.TextAlign.CENTER, color=ft.Colors.OUTLINE),
                    ft.ElevatedButton(
                        "Start Booking Rides",
                        icon=ft.Icons.ADD_LOCATION,
                        on_click=lambda _: page.go("/dashboard"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PRIMARY,
                            color=ft.Colors.ON_PRIMARY
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            else:
                chart_bytes = viz_service.wait_time_chart.get_chart_bytes()
                chart_image = create_chart_image_from_bytes(chart_bytes, "⏱️ Wait Time Distribution")
                chart_container_ref.current.content = chart_image
            page.update()
        except Exception as ex:
            show_error_dialog(f"Failed to generate wait time chart: {str(ex)}")
    
    def show_coverage_chart(e):
        """Show service coverage chart"""
        try:
            result = viz_service.generate_coverage_analysis(current_user, show_plot=False)
            if "error" in result:
                chart_container_ref.current.content = ft.Column([
                    ft.Icon(ft.Icons.MAP, size=100, color=ft.Colors.OUTLINE),
                    ft.Text("🗺️ Service Coverage Analysis", size=24, text_align=ft.TextAlign.CENTER),
                    ft.Text(result["error"], size=16, text_align=ft.TextAlign.CENTER, color=ft.Colors.OUTLINE),
                    ft.ElevatedButton(
                        "Start Booking Rides",
                        icon=ft.Icons.ADD_LOCATION,
                        on_click=lambda _: page.go("/dashboard"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PRIMARY,
                            color=ft.Colors.ON_PRIMARY
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            else:
                chart_bytes = viz_service.coverage_chart.get_chart_bytes()
                chart_image = create_chart_image_from_bytes(chart_bytes, "🗺️ Service Coverage Analysis")
                chart_container_ref.current.content = chart_image
            page.update()
        except Exception as ex:
            show_error_dialog(f"Failed to generate coverage chart: {str(ex)}")
    
    def show_dashboard_chart(e):
        """Show comprehensive dashboard"""
        try:
            result = viz_service.generate_comprehensive_dashboard(current_user, show_plot=False)
            if "error" in result:
                chart_container_ref.current.content = ft.Column([
                    ft.Icon(ft.Icons.DASHBOARD, size=100, color=ft.Colors.OUTLINE),
                    ft.Text("📋 Comprehensive Dashboard", size=24, text_align=ft.TextAlign.CENTER),
                    ft.Text(result["error"], size=16, text_align=ft.TextAlign.CENTER, color=ft.Colors.OUTLINE),
                    ft.ElevatedButton(
                        "Start Booking Rides",
                        icon=ft.Icons.ADD_LOCATION,
                        on_click=lambda _: page.go("/dashboard"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PRIMARY,
                            color=ft.Colors.ON_PRIMARY
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            else:
                chart_bytes = viz_service.dashboard.get_chart_bytes()
                chart_image = create_chart_image_from_bytes(chart_bytes, "📋 Comprehensive Dashboard")
                chart_container_ref.current.content = chart_image
            page.update()
        except Exception as ex:
            show_error_dialog(f"Failed to generate dashboard: {str(ex)}")
    
    def refresh_data(e):
        """Refresh charts with latest real data"""
        try:
            # Just clear the current chart to force refresh on next view
            chart_container_ref.current.content = ft.Column([
                ft.Icon(ft.Icons.REFRESH, size=100, color=ft.Colors.PRIMARY),
                ft.Text("Data Refreshed", size=24, text_align=ft.TextAlign.CENTER),
                ft.Text("Select a chart type to view updated data", size=16, text_align=ft.TextAlign.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            page.update()
            show_success_dialog("Charts refreshed! Select a chart type to view updated data.")
        except Exception as ex:
            show_error_dialog(f"Failed to refresh charts: {str(ex)}")
    
    def show_error_dialog(message: str):
        """Show error dialog"""
        def close_error(e):
            error_dialog.open = False
            page.update()
        
        error_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("❌ Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_error)]
        )
        page.overlay.append(error_dialog)
        error_dialog.open = True
        page.update()
    
    def show_success_dialog(message: str):
        """Show success dialog"""
        def close_success(e):
            success_dialog.open = False
            page.update()
        
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("✅ Success"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_success)]
        )
        page.overlay.append(success_dialog)
        success_dialog.open = True
        page.update()
    
    def show_ride_visualizations(e):
        """Navigate to the ride visualization screen"""
        try:
            # Import and use the new visualization UI
            from app.ui.screens.ride_visualization import create_visualization_page
            
            # Clear current page
            page.controls.clear()
            
            # Add visualization page
            viz_page = create_visualization_page(page)
            page.add(viz_page)
            page.update()
            
        except Exception as ex:
            show_error_dialog(f"Failed to load visualization: {str(ex)}")
    toggleable_logo = container_setup(logo)
    
    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[control_buttons, chart_buttons_row1, chart_buttons_row2],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )
        
    theme_toggle = theme_toggle_button(on_click=handle_theme_click)
    
    title = default_text(DefaultTextStyle.TITLE, "📊 Ride Data Analytics Dashboard")
    
    # Create chart display container with initial welcome message
    initial_content = ft.Column([
        ft.Icon(ft.Icons.ANALYTICS, size=80, color=ft.Colors.BLUE_300),
        ft.Text("Select a chart type to view analytics", size=16, text_align=ft.TextAlign.CENTER),
        ft.Text(f"Analyzing data for: {current_user}", size=14, color=ft.Colors.GREY_600)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    chart_container = ft.Container(
        ref=chart_container_ref,
        content=initial_content,
        bgcolor=ft.Colors.SURFACE,
        border_radius=ft.border_radius.all(12),
        padding=20,
        alignment=ft.alignment.center,
        width=750,
        height=450,
        border=ft.border.all(1, ft.Colors.OUTLINE)
    )
    logout_btn = preset_logout_button(page)
    profile_btn = preset_button(DefaultButton.PROFILE, open_profile(page))
    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    
    # Chart control buttons
    frequency_btn = default_action_button(
        text="📈 Frequency",
        on_click=show_frequency_chart,
        icon=ft.Icons.SHOW_CHART
    )
    
    wait_time_btn = default_action_button(
        text="⏱️ Wait Times",
        on_click=show_wait_time_chart,
        icon=ft.Icons.TIMER
    )
    
    coverage_btn = default_action_button(
        text="🗺️ Coverage",
        on_click=show_coverage_chart,
        icon=ft.Icons.MAP
    )
    
    dashboard_btn = default_action_button(
        text="📋 Dashboard",
        on_click=show_dashboard_chart,
        icon=ft.Icons.DASHBOARD
    )
    
    refresh_btn = default_action_button(
        text="🔄 Refresh Data",
        on_click=refresh_data,
        icon=ft.Icons.REFRESH
    )
    
    show_graphs_ts = default_action_button(
        text="Full Page View",
        on_click=show_ride_visualizations,
        icon=ft.Icons.FULLSCREEN
    )
    
    # Organize chart buttons in rows
    chart_buttons_row1 = default_row(controls=[frequency_btn, wait_time_btn, coverage_btn])
    chart_buttons_row2 = default_row(controls=[dashboard_btn, refresh_btn, show_graphs_ts])
    
    control_buttons = default_row(controls=[profile_btn, logout_btn, back_btn])

    render_page(page, [
        ft.Row([theme_toggle], ft.MainAxisAlignment.END),
        toggleable_logo,
        div(),
        title,
        chart_container,
        div(),
        chart_buttons_row1,
        chart_buttons_row2,
        control_buttons
    ])