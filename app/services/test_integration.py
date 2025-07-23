"""
Integration example showing how the API key configuration works with FastAPI
Run this to test the integration between the Flet app and the API backend
"""
import requests
import json
from app.services.api_config import save_api_key, load_api_key, is_api_configured

def test_api_integration():
    print("🔧 Testing API Key Integration")
    print("=" * 50)
    
    # Check current configuration
    print(f"API Key Configured: {is_api_configured()}")
    
    current_key = load_api_key()
    if current_key:
        print(f"Current API Key: {current_key[:10]}...")
    else:
        print("No API key found in configuration")
    
    # Example: Save a test API key (you would replace with real key)
    test_key = "AIzaSyDummyKeyForTesting123456789012345"
    print(f"\n📝 Saving test API key: {test_key[:10]}...")
    
    if save_api_key(test_key):
        print("✅ API key saved successfully!")
    else:
        print("❌ Failed to save API key")
    
    # Verify it was saved
    loaded_key = load_api_key()
    if loaded_key == test_key:
        print("✅ API key verification successful!")
    else:
        print("❌ API key verification failed")
    
    print(f"\nAPI Configuration Status: {is_api_configured()}")
    
    print("\n🚀 To use with your FastAPI backend:")
    print("1. Start your FastAPI server (uvicorn app.api_test:app --reload)")
    print("2. Configure a real Google Maps API key in the Flet app")
    print("3. Test routes like /route with origin and destination")
    print("4. The FastAPI will automatically use the configured key")

if __name__ == "__main__":
    test_api_integration()
