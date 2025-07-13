import bcrypt

"""
Try to import ENCODING_FORMAT from constants; if it fails, use a default value.
Run encryption.py to test the hashing and verification functions.
"""
try:
    from constants import ENCODING_FORMAT
except (ImportError, ModuleNotFoundError, AttributeError):
    ENCODING_FORMAT = "utf-8"  # Fallback encoding

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(ENCODING_FORMAT), bcrypt.gensalt()).decode(ENCODING_FORMAT)

def verify_password(password: str, hashed: str) -> bool:
    if isinstance(hashed, str):
        hashed = hashed.encode(ENCODING_FORMAT)
    return bcrypt.checkpw(password.encode(ENCODING_FORMAT), hashed)

def test():
    password = "test_password"
    hashed = hash_password(password)
    print(f"Original: {password}")
    print(f"Hashed: {hashed}")
    print(f"Verification: {verify_password(password, hashed)}")
    
if __name__ == "__main__":
    test()
