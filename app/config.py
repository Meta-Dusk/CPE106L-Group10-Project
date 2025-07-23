from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from .env
load_dotenv()

class Config:
    # MongoDB info
    DB_NAME = os.getenv("MONGO_DB_NAME", "ProjectATS")
    COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "accounts")

    # File paths
    ROOT_DIR = Path(os.getenv("ROOT_DIR", "app"))
    SUB_DIR = "auth"
    KEY_PATH = ROOT_DIR / SUB_DIR / "keys" / "secret.key"
    ENC_PATH = ROOT_DIR / SUB_DIR / "enc" / "mongodb.enc"
