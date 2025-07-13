import subprocess
from pathlib import Path
import os
import sys

# Ensure current directory is in PYTHONPATH
env = os.environ.copy()
env["PYTHONPATH"] = str(Path(__file__).parent.resolve())

main_script = Path(__file__).parent / "chaewon_login" / "main.py"

# Prompt the user
print("""
How would you like to run the app?"
[1] Native window (default)"
[2] Web browser
""")
choice = input("Enter choice [1/2] or just press [enter]: ").strip()

# Decide mode
mode_args = []
if choice == "2":
    mode_args = ["--web"]

# Run the Flet app
try:
    subprocess.run(["flet", "run", *mode_args, str(main_script)], check=True, env=env)
except subprocess.CalledProcessError as e:
    print("❌ Flet app failed to run:", e)
    sys.exit(1)
