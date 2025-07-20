import flet as ft

from chaewon_login.ui.components.text import default_text, TextType
from chaewon_login.ui.components.buttons import preset_button, DefaultButton, default_action_button
from chaewon_login.ui.components.containers import div, default_row
from chaewon_login.ui.screens.shared_ui import render_page, preset_logout_button
from chaewon_login.assets.images import default_image, ImageData
from chaewon_login.routing.route_data import PageRoute
from chaewon_login.ride_booking.ride_visuals_utils import visualize_user_rides
"""
TODO: Integrate matplot lib figures into the UI... Somehow.
The current implementation in `handle_viewgraphs()` isn't recommended.
"""

def handle_viewgraphs(page: ft.Page, _):
    def open_profile(e):
        user_id = page.session.get("user_id")
        if user_id:
            page.go(f"/profile/{user_id}")

    msg = default_text(TextType.TITLE, "You are now viewing graphs 🤨")
    image = default_image()
    image.src = ImageData.CHAEWON_SAD.value.path
    insert_here = ft.Container(
        ft.Text(
            value="INSERT GRAPHS HERE 🤔",
            color=ft.Colors.ON_ERROR,
            text_align=ft.TextAlign.CENTER,
            size=40
        ),
        bgcolor=ft.Colors.ERROR,
        alignment=ft.alignment.center,
        adaptive=True,
        expand=True,
        width=800,
        height=400
    )
    logout_btn = preset_logout_button(page)
    profile_btn = preset_button(DefaultButton.PROFILE, open_profile)
    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    show_graphs_ts = default_action_button(
        text="View All Graphs",
        on_click=lambda e: visualize_user_rides("TMTmoney"), # If possible, make a function that just returns a Control instead
        icon=ft.Icons.BAR_CHART
    )
    
    extra_buttons = default_row(controls=show_graphs_ts)
    control_buttons = default_row(controls=[profile_btn, logout_btn, back_btn])

    render_page(page, [
        msg,
        image,
        div(),
        insert_here,
        div(),
        extra_buttons,
        control_buttons
    ])