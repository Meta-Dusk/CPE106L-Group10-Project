import flet as ft
import asyncio

from app.ui.components.text import default_text, DefaultTextStyle
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import div, default_row, default_column
from app.ui.screens.shared_ui import render_page, preset_logout_button, toggle_theme, theme_toggle_button
from app.ui.styles import build_action_button_style
from app.ui.animations import container_setup
from app.assets.images import generate_random_image, update_image_with_random, set_logo
from app.routing.route_data import PageRoute
from app.utils import enable_control_after_delay

"""
Example template for an example handle. Just make sure to only import what you need.
And don't forget to always use `render_page()` at the end of your function, so that it
can render once navigated to.
TIPS:
1. PageRoute is an enum, and when using page.go(), it expects a string, so make sure to add
*.value at the end of the PageRoute enum you want, such as `PageRoute.BOOKING.value`.
2. When putting functions straight into the `on_click` parameter, always use lambda,
but if your function lives in a different script, you can just avoid putting the lambda.
3. If you want a divider rendered in the page, you can just use `div()` instead of ft.Divider()
for simplicity.
4. Refer to assets/images.py on how to add images. Apply image sources by doing
`*.src = ImageData.IMAGE_NAME.value.path`. You can also put image tooltips if you
have declared some in the ImageData enum, by instead doing `*.value.description` and
assigning that to `tooltip`
"""

def handle_booking(page: ft.Page, _):
    title = default_text(DefaultTextStyle.TITLE, "Book a Ride?")
    
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def mod_toggle_theme(e, delay: float = 2.0):
        asyncio.create_task(enable_control_after_delay(control_buttons, delay))
        asyncio.create_task(enable_control_after_delay(example_buttons, delay))
        asyncio.create_task(enable_control_after_delay(theme_toggle, delay))
        await toggle_theme(page, theme_toggle, toggleable_logo, logo, e=e)
        
    theme_toggle = theme_toggle_button(on_click=mod_toggle_theme)
    
    random_image = generate_random_image()
    container_text = ft.Text(
        value="I AM AN EXAMPLE 😔🤚",
        color=ft.Colors.ON_PRIMARY_CONTAINER,
        text_align=ft.TextAlign.CENTER,
        size=40
    )
    
    # If you want a custom container for future stuff, you can just do this:
    example_container = ft.Container(
        content=default_column([
            container_text,
            random_image
        ]),
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        alignment=ft.alignment.center,
        adaptive=True,
        expand=True,
        width=800,
        height=400
    )
    
    logout_btn = preset_logout_button(page)
    back_btn = preset_button(
        type=DefaultButton.BACK,
        on_click=lambda e: page.go(PageRoute.DASHBOARD.value)
    )
        
    test_btn = default_action_button(
        text="Button with custom button style 🤨",
        icon=ft.Icons.INFO,
        style=build_action_button_style(
            primary=ft.Colors.BLACK,
            on_primary=ft.Colors.WHITE,
            primary_highlight=ft.Colors.AMBER,
            seconday_highlight=ft.Colors.GREEN
        ),
        tooltip="I don't do anything 😏",
        on_click=lambda e: update_image_with_random(random_image)
    )
    
    example_buttons = default_row([test_btn])
    control_buttons = default_row([logout_btn, back_btn])
    
    render_page(page, [
        ft.Row([theme_toggle], ft.MainAxisAlignment.END),
        toggleable_logo,
        div(),
        title,
        example_container,
        div(),
        example_buttons,
        control_buttons
    ])