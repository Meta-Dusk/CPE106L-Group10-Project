import inspect
import os
import flet as ft
import asyncio
import json

from pathlib import Path

# == Debug Functions ==
def where_am_i(stack: int = 1):
    frame = inspect.stack()[stack]  # [0] is current function, [1] is caller
    caller_file = frame.filename  # full path to calling file
    return os.path.basename(caller_file)  # just the filename

def get_caller_script():
    for frame_info in inspect.stack():
        filename = os.path.basename(frame_info.filename)
        if filename != os.path.basename(__file__):
            return filename
    return "Unknown"

def print_call_chain():
    print("🔗 Call Chain:")
    stack = inspect.stack()
    for i, frame_info in enumerate(stack[1:]):  # skip this function's own frame
        filename = os.path.basename(frame_info.filename)
        lineno = frame_info.lineno
        func = frame_info.function
        print(f"  {i + 1}. {filename}:{lineno} — {func}()")

def log_button_press(name: str, e: ft.ControlEvent):
    print(f"\"{name}\": button pressed!")


# == Animation Utility
async def enable_control_after_delay(control: ft.Control | list[ft.Control], delay: float):
    # Normalize to list if it's a single control
    controls = control if isinstance(control, list) else [control]

    # Disable all controls and update
    for c in controls:
        c.disabled = True
        c.update()

    await asyncio.sleep(delay)

    # Re-enable all controls and update
    for c in controls:
        c.disabled = False
        c.update()


# == Other Stuff ==
def milliseconds_to_seconds(ms: int):
    return ms / 1000


# == Launcher Config ==
LAUNCHER_CONFIG_PATH = Path(__file__).parent / "ui" / "configs" / "launcher_config.json"

def save_launcher_config(
    launch_mode: str,
    window_mode: str,
    file_path: Path = LAUNCHER_CONFIG_PATH
):
    config_data = {
        "launch_mode": launch_mode,
        "window_mode": window_mode
    }

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        print(f"✅ Config saved to {file_path}")
    except Exception as e:
        print(f"❌ Failed to save config: {e}")

def load_launcher_config(file_path: Path = LAUNCHER_CONFIG_PATH) -> dict:
    if not file_path.exists():
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        return config_data
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return {}


# == Utils Test ==
def test():
    print(f"Called from: {where_am_i()}")
    
if __name__ == "__main__":
    test()