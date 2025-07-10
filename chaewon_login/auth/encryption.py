import bcrypt
from constants import ENCODING_FORMAT

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(ENCODING_FORMAT), bcrypt.gensalt()).decode(ENCODING_FORMAT)

def verify_password(password: str, hashed: str) -> bool:
    if isinstance(hashed, str):
        hashed = hashed.encode(ENCODING_FORMAT)
    return bcrypt.checkpw(password.encode(ENCODING_FORMAT), hashed)
