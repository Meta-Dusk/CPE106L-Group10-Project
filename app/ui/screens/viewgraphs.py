import flet as ft
import asyncio

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import div, default_row, default_column
from app.ui.screens.shared_ui import render_page, preset_logout_button, open_profile, toggle_theme, theme_toggle_button
from app.ui.animations import container_setup
from app.assets.images import set_logo
from app.routing.route_data import PageRoute
from app.ride_booking.ride_visuals_utils import visualize_user_rides
from app.utils import enable_control_after_delay

"""
TODO: Integrate matplot lib figures into the UI... Somehow.
The current implementation in `handle_viewgraphs()` isn't recommended.
"""

def handle_viewgraphs(page: ft.Page, _):
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def mod_toggle_theme(e, delay: float = 2.0):
        asyncio.create_task(enable_control_after_delay(control_buttons, delay))
        asyncio.create_task(enable_control_after_delay(extra_buttons, delay))
        await toggle_theme(page, theme_toggle, toggleable_logo, logo, e=e)
        
    theme_toggle = theme_toggle_button(on_click=mod_toggle_theme)
    
    title = default_text(DefaultTextStyle.TITLE, "You are now viewing graphs 🤨")
    
    container_text = ft.Text(
        value="INSERT GRAPHS HERE 🤔",
        color=ft.Colors.ON_ERROR,
        text_align=ft.TextAlign.CENTER,
        size=40
    )
    messages = [
        default_text(DefaultTextStyle.DEFAULT, "I am a DEFAULT-type text"),
        default_text(DefaultTextStyle.TITLE, "I am a TITLE-type text"),
        default_text(DefaultTextStyle.SUBTITLE, "I am a SUBTITLE-type text."),
        default_text(DefaultTextStyle.ERROR, "I am an ERROR-type text.")
    ]
    column_text = default_column()
    for text in messages:
        column_text.controls.append(text)
    
    example_container = ft.Container(
        content=container_text,
        bgcolor=ft.Colors.ERROR,
        alignment=ft.alignment.center,
        adaptive=True,
        expand=True,
        width=800,
        height=400
    )
    logout_btn = preset_logout_button(page)
    profile_btn = preset_button(DefaultButton.PROFILE, open_profile(page))
    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    show_graphs_ts = default_action_button(
        text="View All Graphs",
        on_click=lambda e: visualize_user_rides("TMTmoney"), # If possible, make a function that just returns a Control instead
        icon=ft.Icons.BAR_CHART
    )
    
    extra_buttons = default_row(controls=show_graphs_ts)
    control_buttons = default_row(controls=[profile_btn, logout_btn, back_btn])

    render_page(page, [
        ft.Row([theme_toggle], ft.MainAxisAlignment.END),
        toggleable_logo,
        div(),
        title,
        example_container,
        column_text,
        div(),
        extra_buttons,
        control_buttons
    ])