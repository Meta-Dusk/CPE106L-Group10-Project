import json
from pathlib import Path
import flet as ft

CONFIG_FILE_DIR = Path(__file__).parent / "configs"
CONFIG_FILE = CONFIG_FILE_DIR  / "theme_config.json"

def save_theme_mode(mode: ft.ThemeMode):
    CONFIG_FILE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"theme_mode": mode.value}, f)
        

def load_theme_mode() -> ft.ThemeMode:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            try:
                data = json.load(f)
                return ft.ThemeMode(data.get("theme_mode", "light"))
            except:
                pass
    return ft.ThemeMode.DARK
