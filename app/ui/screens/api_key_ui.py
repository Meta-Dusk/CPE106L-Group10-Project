import flet as ft

from app.ui.components.containers import default_column, div, default_row
from app.ui.components.text import default_text, DefaultTextStyle, default_input_field, DefaultInputFieldType
from app.ui.components.buttons import default_action_button, preset_button, DefaultButton
from app.ui.screens.shared_ui import render_page, theme_toggle_button, mod_toggle_theme, StatusMessage
from app.services.api_config import save_api_key, load_api_key, validate_api_key, is_api_configured, clear_api_config
from app.routing.route_data import PageRoute
from app.assets.images import set_logo
from app.ui.animations import container_setup


def handle_api_key_entry(page: ft.Page, _):    
    # Check if API key is already configured
    current_api_key = load_api_key()
    is_configured = is_api_configured()
    
    # Title
    title = default_text(DefaultTextStyle.TITLE, "Google Maps API Configuration")
    
    description = default_text(DefaultTextStyle.SUBTITLE, "...")
    
    # API Key input field
    api_key_input = default_input_field(input_field_type=DefaultInputFieldType.API_KEY)
    if current_api_key:
        # Show masked version of current key
        api_key_input.value = current_api_key[:10] + "..." if len(current_api_key) > 10 else current_api_key
    
    # Status message
    status_message = ft.Text(value="", size=16)
    status = StatusMessage(status_message)
    
    def update_description(description_control: ft.Text):
        if is_api_configured():
            description_text = (
                "✅ API key is currently configured and active.\n"
                "You can update it below or clear the current configuration."
            )
        else:
            description_text = (
                "Configure your Google Maps API key for route calculation and mapping features.\n"
                "You can get your API key from the Google Cloud Console."
            )
        description_control.value = description_text
        description_control.update()
    
    def set_error(message: str):
        api_key_input.error_text = message
        api_key_input.update()
    
    def clear_error():
        api_key_input.error_text = ""
        api_key_input.update()
    
    def on_save(e):
        """Handle save API key"""
        api_key = api_key_input.value
        
        if not api_key or api_key.strip() == "":
            set_error("API Key is required")
            status.error("Please enter a valid API key")
            return
        
        api_key = api_key.strip()
        
        if not validate_api_key(api_key):
            set_error("Invalid API key format")
            status.error("Invalid API key format. Please check your key.")
            return
        
        # Clear any previous errors
        clear_error()
        
        # Save the API key
        if save_api_key(api_key):
            status.success(f"✅ API key saved successfully! Key: {api_key[:8]}...")
            # print(f"🔑 API Key configured: {api_key}") # That's a security issue 💀
            
            # Update button states
            update_button_states(True)
        else:
            status.error("❌ Failed to save API key. Please try again.")
        update_description(description)
    
    def clear_values(e):
        api_key_input.value = ""
        clear_error()
        status_message.value = ""
    
    def on_clear(e):
        """Handle clear API key input"""
        clear_values(e)
        page.update()
    
    def on_remove_config(e):
        """Handle remove API configuration"""
        if clear_api_config():
            clear_values(e)
            status.info("🗑️ API configuration cleared successfully")
            update_button_states(False)
        else:
            status.error("❌ Failed to clear API configuration")
        update_description(description)
    
    def on_test_connection(e):
        """Test API key by making a simple request"""
        status.info("🔄 Testing API key with Google Maps API...")
        
        api_key = load_api_key()
        if not api_key:
            status.error("❌ No API key configured to test")
            return
        
        # Test with a simple geocoding request
        import requests
        test_url = "https://maps.googleapis.com/maps/api/geocode/json"
        test_params = {
            "address": "Manila, Philippines",
            "key": api_key
        }
        
        try:
            response = requests.get(test_url, params=test_params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OK":
                    status.success("✅ API key is valid and working!")
                elif data.get("status") == "REQUEST_DENIED":
                    status.error("❌ API key is invalid or lacks permissions")
                else:
                    status.error(f"❌ API test failed: {data.get('status', 'Unknown error')}")
            else:
                status.error(f"❌ HTTP error: {response.status_code}")
        except requests.RequestException as e:
            status.error(f"❌ Network error: {str(e)}")
        except Exception as e:
            status.error(f"❌ Test failed: {str(e)}")
    
    def on_back_to_dashboard(e):
        """Navigate back to dashboard"""
        page.go(PageRoute.DASHBOARD.value)
    
    def update_button_states(configured: bool):
        """Update button visibility based on configuration state"""
        remove_btn.visible = configured
        test_btn.visible = configured
        page.update()
    
    # Buttons
    save_button = default_action_button(
        text="Save API Key",
        on_click=on_save,
        icon=ft.Icons.SAVE,
        tooltip="Save the Google Maps API key"
    )
    
    clear_button = default_action_button(
        text="Clear",
        on_click=on_clear,
        icon=ft.Icons.CLEAR,
        tooltip="Clear the input field"
    )
    
    remove_btn = default_action_button(
        text="Remove Config",
        on_click=on_remove_config,
        icon=ft.Icons.DELETE,
        tooltip="Remove the current API configuration"
    )
    remove_btn.visible = is_configured
    
    test_btn = default_action_button(
        text="Test API",
        on_click=on_test_connection,
        icon=ft.Icons.NETWORK_CHECK,
        tooltip="Test the API key connection"
    )
    test_btn.visible = is_configured
    
    back_button = preset_button(
        DefaultButton.BACK,
        on_click=on_back_to_dashboard
    )
    
    # Button rows
    main_buttons = default_row([save_button, clear_button])
    
    config_buttons = default_row([remove_btn, test_btn])
    
    back_row = default_row([back_button])
    
    # Logo + Theme Switch
    logo = set_logo()
    toggleable_logo = container_setup(logo)
    
    async def handle_theme_click(e):
        await mod_toggle_theme(
            e, page, toggle_controls=[top_row, config_buttons, back_row, main_buttons],
            toggleable_logo=toggleable_logo, theme_toggle=theme_toggle, logo=logo
        )
        
    theme_toggle = theme_toggle_button(on_click=handle_theme_click)
    
    top_row = ft.Row([theme_toggle], ft.MainAxisAlignment.END)
    
    description_container = ft.Container(
        content=description,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        border_radius=ft.border_radius.all(20),
        adaptive=True,
        padding=ft.padding.all(10)
    )
    
    # Main content column
    content = default_column(
        controls=[
            top_row,
            toggleable_logo,
            div(),  # Spacing
            title,
            description_container,
            div(),  # Spacing
            status_message,
            api_key_input,
            main_buttons,
            config_buttons,
            div(),  # Spacing
            back_row
        ]
    )
    
    # Render the page
    render_page(page, content)
    update_description(description)
    