import flet as ft
import asyncio
import re

from app.routing.route_data import PageRoute
from app.db.db_manager import find_user, update_user
from app.ui.components.text import default_text, DefaultTextStyle, mod_input_field
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import div, default_row
from app.ui.screens.shared_ui import render_page, preset_logout_button, toggle_theme, theme_toggle_button
from app.assets.images import set_logo
from app.ui.animations import container_setup
from app.utils import enable_control_after_delay
from datetime import datetime


def handle_profile(page: ft.Page, e: ft.RouteChangeEvent, user_id: str):
    user_doc = find_user(user_id)
    
    def on_date_picker_change(e):
        dob_field.value = date_picker.value.strftime("%Y-%m-%d")
        page.update()
        
    def on_date_picker_dismiss(e):
        page.close(date_picker)
    
    date_picker = ft.DatePicker(
        first_date=datetime(year=2000, month=1, day=1),
        last_date=datetime.now(),
        on_change=on_date_picker_change,
        on_dismiss=on_date_picker_dismiss,
    )
    
    # Fields
    full_name_field = mod_input_field(label="Full Name")
    address_field = mod_input_field(label="Home Address")
    dob_field = mod_input_field(
        label="Date of Birth",
        read_only=True,
        suffix=ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(date_picker),
            icon_color=ft.Colors.PRIMARY
        ),
    )
    
    def format_phone_number(e):
        raw = re.sub(r"\D", "", e.control.value or "")  # Remove non-digit characters
        raw = raw[:10] # Limit to 10 digits

        # Apply formatting: 0912-345-6789
        formatted = raw
        if len(raw) >= 4:
            formatted = raw[:4]
            if len(raw) >= 7:
                formatted += "-" + raw[4:7] + "-" + raw[7:]
            elif len(raw) > 4:
                formatted += "-" + raw[4:]
        
        if e.control.value != formatted:
            phone_field.value = formatted
            page.update()
        
    phone_field = mod_input_field(
        label="Phone Number",
        prefix_text="+63",
        max_length=16,
        on_change=format_phone_number
    )
    email_field = mod_input_field(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    
    def validate_fields(e):
        reset_errors(e)
        
        # Sanitize phone number (remove dashes and spaces)
        raw_phone = re.sub(r"\D", "", phone_field.value or "")
        
        # Validate required fields
        if not full_name_field.value.strip():
            full_name_field.error_text = "Full name is required."
        if not address_field.value.strip():
            address_field.error_text = "Home address is required."
        if not dob_field.value.strip():
            dob_field.error_text = "Date of birth is required."
        if not raw_phone or len(raw_phone) != 10:
            phone_field.error_text = "Phone number must be 10 digits."
        if not email_field.value.strip():
            email_field.error_text = "Email is required."

        # Validate email format
        elif not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email_field.value.strip()):
            email_field.error_text = "Invalid email address."

        page.update()
        
        for i in [full_name_field, address_field, dob_field, phone_field, email_field]:
            if i.error_text:
                return
        
        success = update_user(
            filter_query={"username": user_doc["username"]},
            updated_fields={
                "full_name": full_name_field.value.strip(),
                "address": address_field.value.strip(),
                "date_of_birth": dob_field.value.strip(),
                "phone": phone_field.value.strip(),
                "email": email_field.value.strip()
            }
        )
        if success:
            print(f"✅ User \"{user_doc['username']}\" successfully updated!")
        else:
            print("⚠️ No matching user found to update.")
    
    submit_button = default_action_button(text="Save Profile", on_click=validate_fields)
    
    input_fields = [
        full_name_field,
        address_field,
        dob_field,
        phone_field,
        email_field
    ]
    
    def reset_errors(e):
        for i in input_fields:
            i.error_text = ""
                
    reset_errors(e)

    if user_doc:
        title = default_text(DefaultTextStyle.TITLE, f"{user_doc['username']}'s Profile")
        subtitle = default_text(DefaultTextStyle.SUBTITLE, "Welcome back!" if not user_doc['op'] else "Greetings, admin.")
        full_name_field.value = user_doc.get("full_name", "")
        address_field.value = user_doc.get("address", "")
        dob_field.value = user_doc.get("date_of_birth", "")  # Expected to be "YYYY-MM-DD"
        phone_field.value = user_doc.get("phone", "")
        email_field.value = user_doc.get("email", "")
    else:
        title = default_text(DefaultTextStyle.TITLE, "User not found 😢")
        subtitle = default_text(DefaultTextStyle.SUBTITLE, f"User ID: {user_id}")
    
    card_text = ft.Text("Edit Profile", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    
    # Card UI layout
    profile_card_column = ft.Column(
        controls=[card_text],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    profile_card_column.controls.extend(input_fields)
    profile_card_column.controls.extend(submit_button)
    
    profile_card = ft.Card(
        content=ft.Container(
            content=profile_card_column,
            padding=20,
            width=450,
        ),
        elevation=4,
    )
    
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def mod_toggle_theme(e, delay: float = 2.0):
        asyncio.create_task(enable_control_after_delay(control_buttons, delay))
        asyncio.create_task(enable_control_after_delay(theme_toggle, delay))
        await toggle_theme(page, theme_toggle, toggleable_logo, logo, e=e)
        
    theme_toggle = theme_toggle_button(on_click=mod_toggle_theme)

    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    logout_btn = preset_logout_button(page)

    control_buttons = default_row(controls=[logout_btn, back_btn])

    render_page(page, [
        ft.Row([theme_toggle], ft.MainAxisAlignment.END),
        toggleable_logo,
        div(),
        title,
        subtitle,
        profile_card,
        div(),
        control_buttons
    ])
