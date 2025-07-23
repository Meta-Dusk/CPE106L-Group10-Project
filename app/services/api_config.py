"""
API Configuration Service
Handles Google Maps API key storage and retrieval
"""
import json
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet

CONFIG_DIR = Path(__file__).parent.parent / "storage" / "data"
API_CONFIG_FILE = CONFIG_DIR / "api_config.json"
KEY_FILE = Path(__file__).parent.parent / "auth" / "keys" / "secret.key"

def ensure_config_dir():
    """Ensure the config directory exists"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_encryption_key() -> bytes:
    """Load or generate encryption key"""
    if KEY_FILE.exists():
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    else:
        # Generate new key if it doesn't exist
        key = Fernet.generate_key()
        KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        return key

def encrypt_data(data: str) -> str:
    """Encrypt sensitive data"""
    key = load_encryption_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt sensitive data"""
    key = load_encryption_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

def save_api_key(api_key: str) -> bool:
    """Save Google Maps API key securely"""
    try:
        ensure_config_dir()
        
        # Load existing config or create new
        config = {}
        if API_CONFIG_FILE.exists():
            with open(API_CONFIG_FILE, 'r') as f:
                config = json.load(f)
        
        # Encrypt and save API key
        config['google_maps_api_key'] = encrypt_data(api_key)
        config['configured'] = True
        
        with open(API_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving API key: {e}")
        return False

def load_api_key() -> Optional[str]:
    """Load Google Maps API key"""
    try:
        if not API_CONFIG_FILE.exists():
            return None
        
        with open(API_CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        if 'google_maps_api_key' not in config:
            return None
        
        return decrypt_data(config['google_maps_api_key'])
    except Exception as e:
        print(f"Error loading API key: {e}")
        return None

def is_api_configured() -> bool:
    """Check if API key is configured"""
    try:
        if not API_CONFIG_FILE.exists():
            return False
        
        with open(API_CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        return config.get('configured', False) and 'google_maps_api_key' in config
    except Exception:
        return False

def validate_api_key(api_key: str) -> bool:
    """Validate API key format (basic validation)"""
    if not api_key or len(api_key.strip()) == 0:
        return False
    
    # Basic Google API key format validation
    # Google API keys are typically 39 characters long and start with 'AIza'
    api_key = api_key.strip()
    if len(api_key) == 39 and api_key.startswith('AIza'):
        return True
    
    # Allow for other valid formats or test keys
    if len(api_key) >= 20:  # Minimum length for API keys
        return True
    
    return False

def clear_api_config():
    """Clear API configuration"""
    try:
        if API_CONFIG_FILE.exists():
            API_CONFIG_FILE.unlink()
        return True
    except Exception as e:
        print(f"Error clearing API config: {e}")
        return False
