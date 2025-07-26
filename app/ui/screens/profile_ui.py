import flet as ft
import re
import asyncio

from app.assets.audio_manager import audio, SFX
from app.assets.images import set_logo
from app.db.db_manager import find_user, update_user, check_matching_document
from app.ui.components.text import default_text, DefaultTextStyle, mod_input_field
from app.ui.components.buttons import preset_button, DefaultButton, default_action_button
from app.ui.components.containers import div, default_row, spaced_buttons
from app.ui.components.dialogs import default_notif_dialog, show_auto_closing_dialog
from app.ui.screens.shared_ui import (
    render_page, preset_logout_button, mod_toggle_theme, theme_toggle_button, preset_exit_button,
    open_op)
from app.ui.animations import container_setup
from app.utils import format_raw_phone
from app.routing.route_data import PageRoute
from datetime import datetime


def handle_profile(page: ft.Page, e: ft.RouteChangeEvent, user_id: str):
    user_doc = find_user(user_id)
    
    def on_date_picker_change(e):
        audio.play_sfx(SFX.NOTIF)
        dob_field.value = date_picker.value.strftime("%Y-%m-%d")
        page.update()
        
    def on_date_picker_dismiss(e):
        audio.play_sfx(SFX.CLICK)
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
        formatted = format_raw_phone(e.control.value)
        if e.control.value != formatted:
            phone_field.value = formatted
            page.update()
        
    phone_field = mod_input_field(
        label="Phone Number",
        prefix_text="(+63)",
        max_length=18,
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
                audio.play_sfx(SFX.ERROR)
                return
        
        formatted_phone = f"+63{raw_phone}"
        
        check = check_matching_document(
            filter_query={"username": user_doc["username"]},
            value_checks={
                "full_name": full_name_field.value.strip(),
                "address": address_field.value.strip(),
                "date_of_birth": dob_field.value.strip(),
                "phone": formatted_phone,
                "email": email_field.value.strip()
            }
        )
        
        if not check:
            success = update_user(
                filter_query={"username": user_doc["username"]},
                updated_fields={
                    "full_name": full_name_field.value.strip(),
                    "address": address_field.value.strip(),
                    "date_of_birth": dob_field.value.strip(),
                    "phone": formatted_phone,
                    "email": email_field.value.strip()
                }
            )
        else:
            success = False
            
        if success:
            audio.play_sfx(SFX.REWARD)
            print(f"✅ User \"{user_doc['username']}\" successfully updated!")
            dialog_title = default_text(DefaultTextStyle.TITLE, "User Updated")
            dialog_content = default_text(DefaultTextStyle.SUBTITLE, f"{user_doc['username']}'s details successfully updated!")
            dialog_icon = ft.Icon(name=ft.Icons.INFO_ROUNDED, color=ft.Colors.PRIMARY, size=50)
        elif not success and check:
            audio.play_sfx(SFX.NOTIF)
            print(f"Nothing to update for user \"{user_doc['username']}\"")
            dialog_title = default_text(DefaultTextStyle.TITLE, "No Updates")
            dialog_content = default_text(DefaultTextStyle.SUBTITLE, f"Nothing to update for {user_doc['username']}'s details.")
            dialog_icon = ft.Icon(name=ft.Icons.INFO_ROUNDED, color=ft.Colors.PRIMARY, size=50)
        else:
            audio.play_sfx(SFX.ERROR)
            print("⚠️ No matching user found to update.")
            dialog_title = default_text(DefaultTextStyle.TITLE, "User Error")
            dialog_content = default_text(DefaultTextStyle.ERROR, "No matching user found to update.")
            dialog_icon = ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.ERROR, size=50)
        
        dialog = default_notif_dialog(
            title=dialog_title,
            icon=dialog_icon,
            content=dialog_content
        )
        
        asyncio.run(show_auto_closing_dialog(page, dialog, 2.0))
    
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
        
        # Format and apply phone
        raw_phone = user_doc.get("phone", "").removeprefix("+63")  # Remove +63 prefix
        phone_field.value = format_raw_phone(raw_phone)
        
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
    profile_card_column.controls.extend([submit_button])
    
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
    
    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[control_buttons, theme_toggle, submit_button],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )
        
    theme_toggle = theme_toggle_button(on_click=handle_theme_click)

    back_btn = preset_button(DefaultButton.BACK, lambda e: page.go(PageRoute.DASHBOARD.value))
    logout_btn = preset_logout_button(page)
    
    op_btn = default_action_button(
        text="Operator Control Center",
        icon=ft.Icons.ADMIN_PANEL_SETTINGS,
        on_click=open_op(page),
        tooltip="Show Operator Control Center (ADMIN ONLY)",
        visible=True if user_doc['op'] else False
    )

    control_buttons = default_row(controls=[logout_btn, back_btn, op_btn])
    
    exit_btn = preset_exit_button(page)
    
    top_row = spaced_buttons([exit_btn], [theme_toggle])

    render_page(page, [
        top_row,
        toggleable_logo,
        div(),
        title,
        subtitle,
        profile_card,
        div(),
        control_buttons
    ])
