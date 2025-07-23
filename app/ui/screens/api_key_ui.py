import flet as ft

from app.ui.components.containers import default_column, div, default_row
from app.ui.components.text import default_text, DefaultTextStyle, default_input_field, DefaultInputFieldType
from app.ui.components.buttons import default_action_button, preset_button, DefaultButton
from app.ui.screens.shared_ui import render_page
from app.services.api_config import save_api_key, load_api_key, validate_api_key, is_api_configured, clear_api_config
from app.routing.route_data import PageRoute


def handle_api_key_entry(page: ft.Page, _):    
    # Check if API key is already configured
    current_api_key = load_api_key()
    is_configured = is_api_configured()
    
    # Title
    title = default_text(DefaultTextStyle.TITLE, "Google Maps API Configuration")
    
    # Description
    description_text = (
        "Configure your Google Maps API key for route calculation and mapping features.\n"
        "You can get your API key from the Google Cloud Console."
    )
    
    if is_configured:
        description_text = (
            "✅ API key is currently configured and active.\n"
            "You can update it below or clear the current configuration."
        )
    
    description = default_text(DefaultTextStyle.SUBTITLE, description_text)
    
    # API Key input field
    api_key_input = default_input_field(input_field_type=DefaultInputFieldType.API_KEY)
    if current_api_key:
        # Show masked version of current key
        api_key_input.value = current_api_key[:10] + "..." if len(current_api_key) > 10 else current_api_key
    
    # Status message
    status_message = ft.Text(value="", size=16)
    
    def show_success(message: str):
        status_message.value = message
        status_message.color = ft.Colors.GREEN
        page.update()
    
    def show_error(message: str):
        status_message.value = message
        status_message.color = ft.Colors.RED
        page.update()
    
    def show_info(message: str):
        status_message.value = message
        status_message.color = ft.Colors.BLUE
        page.update()
    
    def on_save(e):
        """Handle save API key"""
        api_key = api_key_input.value
        
        if not api_key or api_key.strip() == "":
            api_key_input.error_text = "API Key is required"
            show_error("Please enter a valid API key")
            return
        
        api_key = api_key.strip()
        
        if not validate_api_key(api_key):
            api_key_input.error_text = "Invalid API key format"
            show_error("Invalid API key format. Please check your key.")
            return
        
        # Clear any previous errors
        api_key_input.error_text = ""
        
        # Save the API key
        if save_api_key(api_key):
            show_success(f"✅ API key saved successfully! Key: {api_key[:4]}...")
            # print(f"🔑 API Key configured: {api_key}") # That's a security issue 💀
            
            # Update button states
            update_button_states(True)
        else:
            show_error("❌ Failed to save API key. Please try again.")
    
    def on_clear(e):
        """Handle clear API key input"""
        api_key_input.value = ""
        api_key_input.error_text = ""
        status_message.value = ""
        page.update()
    
    def on_remove_config(e):
        """Handle remove API configuration"""
        if clear_api_config():
            show_info("🗑️ API configuration cleared successfully")
            api_key_input.value = ""
            api_key_input.error_text = ""
            update_button_states(False)
        else:
            show_error("❌ Failed to clear API configuration")
    
    def on_test_connection(e):
        """Test API key by making a simple request"""
        show_info("🔄 Testing API key with Google Maps API...")
        
        api_key = load_api_key()
        if not api_key:
            show_error("❌ No API key configured to test")
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
                    show_success("✅ API key is valid and working!")
                elif data.get("status") == "REQUEST_DENIED":
                    show_error("❌ API key is invalid or lacks permissions")
                else:
                    show_error(f"❌ API test failed: {data.get('status', 'Unknown error')}")
            else:
                show_error(f"❌ HTTP error: {response.status_code}")
        except requests.RequestException as e:
            show_error(f"❌ Network error: {str(e)}")
        except Exception as e:
            show_error(f"❌ Test failed: {str(e)}")
    
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
    
    # Main content column
    content = default_column(
        controls=[
            title,
            div(),  # Spacing
            description,
            div(),  # Spacing
            api_key_input,
            status_message,
            div(),  # Spacing
            main_buttons,
            config_buttons,
            div(),  # Spacing
            back_row
        ]
    )
    
    # # Container with proper alignment and spacing
    # container = default_container(content)
    
    # Render the page
    render_page(page, content)
