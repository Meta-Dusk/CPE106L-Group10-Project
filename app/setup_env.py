from pathlib import Path
import shutil

def setup_env():
    # Get the current directory
    base_dir = Path(__file__).resolve().parent

    # Define paths
    env_sample_path = base_dir / ".env.sample"
    env_path = base_dir / ".env"

    # Check if .env already exists
    if env_path.exists():
        print(".env file already exists.")
        return

    # Check if .env.sample exists and copy it
    if env_sample_path.exists():
        shutil.copy(env_sample_path, env_path)
        print(".env created from .env.sample.")
    else:
        print("Error: .env.sample file not found.")

if __name__ == "__main__":
    setup_env()
