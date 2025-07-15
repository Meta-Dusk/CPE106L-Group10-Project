import subprocess
import os
import sys
import tkinter as tk

from pathlib import Path
from tkinter import messagebox
from chaewon_login.setup import setup_gui
from chaewon_login.ui.styles import TKINTER
from chaewon_login.ui.components import default_root_window

# === Setup environment ===
env = os.environ.copy()
env["PYTHONPATH"] = str(Path(__file__).parent.resolve())
main_script = Path(__file__).parent / "chaewon_login" / "main.py"

BG_COLOR = TKINTER.DEFAULT_BG_COLOR.value
FG_COLOR = TKINTER.DEFAULT_FG_COLOR.value
ACCENT_COLOR = TKINTER.DEFAULT_ACCENT_COLOR.value
CANCEL_COLOR = TKINTER.DEFAULT_CANCEL_COLOR.value
RADIO_BG = TKINTER.DEFAULT_RADIO_BG.value

root = default_root_window(
    title="Chaewon App Launcher",
    width=340,
    height=200
)

def disable_buttons():
    launch_button.config(state="disabled")
    cancel_button.config(state="disabled")

# === Launch app based on selected mode ===
def run_app(mode: str):
    disable_buttons()
    root.update_idletasks() # Reflect disabled state before closing
    root.destroy()          # Close launcher

    if mode == "setup":
        setup_gui()
        messagebox.showinfo("Setup Complete", "Setup has been completed.")
        return

    mode_args = ["--web"] if mode == "web" else []

    try:
        subprocess.run(["flet", "run", *mode_args, str(main_script)], check=True, env=env)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Flet app failed to run:\n{e}")
        sys.exit(1)

def on_submit():
    selected = var.get()
    run_app(selected)

def on_cancel():
    disable_buttons()
    root.destroy()

# === Shared control state ===
var = tk.StringVar(value="native")

# === Styled radio button helper ===
def create_radio(text, value):
    return tk.Radiobutton(
        root,
        text=text,
        variable=var,
        value=value,
        bg=RADIO_BG,
        fg=FG_COLOR,
        selectcolor=BG_COLOR,
        activebackground=RADIO_BG,
        activeforeground=FG_COLOR,
        anchor="w",
        justify="left"
    )

# === UI Components ===
tk.Label(root, text="How would you like to run the app?", font=("Arial", 12), fg=FG_COLOR, bg=BG_COLOR).pack(pady=15)

create_radio("Native window (default)", "native").pack(anchor="w", padx=30)
create_radio("Web browser", "web").pack(anchor="w", padx=30)
create_radio("Run setup", "setup").pack(anchor="w", padx=30)

btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=25)

launch_button = tk.Button(btn_frame, text="Launch", command=on_submit,
                          bg=ACCENT_COLOR, fg="white", width=12, relief="raised")
launch_button.pack(side="left", padx=10)

cancel_button = tk.Button(btn_frame, text="Cancel", command=on_cancel,
                          bg=CANCEL_COLOR, fg="white", width=12, relief="raised")
cancel_button.pack(side="left", padx=10)

root.mainloop()
