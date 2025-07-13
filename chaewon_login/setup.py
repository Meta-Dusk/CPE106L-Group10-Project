from config import Config
from cryptography.fernet import Fernet
import getpass
import sys
import shutil

def ensure_directories():
    for path in [Config.KEY_PATH, Config.ENC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)

def generate_key():
    key = Fernet.generate_key()
    Config.KEY_PATH.write_bytes(key)
    return key

def encrypt_uri(key: bytes, uri: str):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(uri.encode())
    Config.ENC_PATH.write_bytes(encrypted)

def delete_directories():
    # Delete the entire key and enc directories (parents of the files)
    try:
        shutil.rmtree(Config.KEY_PATH.parent)
        shutil.rmtree(Config.ENC_PATH.parent)
        print("🗑️ Previous key and encrypted files deleted.")
    except Exception as e:
        print(f"❌ Failed to delete directories: {e}")
        sys.exit(1)

def prompt_reset():
    print(f"""
[!] Setup already completed.
🔑 Key path: {Config.KEY_PATH}
🔒 Encrypted URI: {Config.ENC_PATH}
""")
    choice = input("Do you want to reset the setup and delete these files? (y/n): ").lower()
    return choice == "y"

def setup():
    if Config.KEY_PATH.exists() or Config.ENC_PATH.exists():
        if not prompt_reset():
            print("⚠️ Setup canceled. No changes were made.")
            return
        delete_directories()

    print("🔐 MongoDB Setup Utility")

    ensure_directories()

    try:
        mongodb_uri = getpass.getpass("Enter your MongoDB URI (input hidden): ").strip()
    except KeyboardInterrupt:
        print("\nSetup canceled.")
        sys.exit(1)

    if not mongodb_uri:
        print("❌ MongoDB URI cannot be empty.")
        return

    print("🔑 Generating encryption key...")
    key = generate_key()

    print("🛡️ Encrypting MongoDB URI...")
    encrypt_uri(key, mongodb_uri)

    print(f"""
✅ Setup complete!
🔒 Encrypted URI saved to: {Config.ENC_PATH}
🔑 Key saved to: {Config.KEY_PATH}
⚠️  Remember to exclude these from version control (already in .gitignore)
""")

if __name__ == "__main__":
    setup()
