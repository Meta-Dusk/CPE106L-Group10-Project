import tkinter as tk
import shutil

from tkinter import messagebox
from chaewon_login.config import Config
from cryptography.fernet import Fernet
from chaewon_login.setup_env import setup_env
from chaewon_login.ui.styles import TKINTER
from chaewon_login.ui.components import default_root_window

BG_COLOR = TKINTER.DEFAULT_BG_COLOR.value
FG_COLOR = TKINTER.DEFAULT_FG_COLOR.value
ACCENT_COLOR = TKINTER.DEFAULT_ACCENT_COLOR.value
CANCEL_COLOR = TKINTER.DEFAULT_CANCEL_COLOR.value

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
    try:
        shutil.rmtree(Config.KEY_PATH.parent)
        shutil.rmtree(Config.ENC_PATH.parent)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete directories:\n{e}")
        return False

def reset_prompt():
    return messagebox.askyesno(
        "Setup Already Exists",
        f"A previous setup already exists.\n\nDo you want to reset it?"
    )

def handle_setup(mongo_entry, root):
    mongodb_uri = mongo_entry.get().strip()

    if not mongodb_uri:
        messagebox.showerror("Input Error", "MongoDB URI cannot be empty.")
        return

    setup_env()

    if Config.KEY_PATH.exists() or Config.ENC_PATH.exists():
        if not reset_prompt():
            messagebox.showinfo("Setup Canceled", "Setup canceled. No changes were made.")
            return
        if not delete_directories():
            return

    ensure_directories()

    key = generate_key()
    encrypt_uri(key, mongodb_uri)

    messagebox.showinfo("Setup Complete", "MongoDB credentials have been encrypted and saved successfully.")

    root.destroy()


def setup_gui():
    root = default_root_window(
        title="Chaewon Setup",
        width=420,
        height=160
    )

    tk.Label(root, text="MongoDB URI Setup", font=("Arial", 14), fg=FG_COLOR, bg=BG_COLOR).pack(pady=10)
    tk.Label(root, text="Enter your MongoDB URI:", fg=FG_COLOR, bg=BG_COLOR).pack()

    mongo_entry = tk.Entry(root, width=50, show="*", bg="#333", fg=FG_COLOR, insertbackground=FG_COLOR)
    mongo_entry.pack(pady=5)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=15)

    tk.Button(button_frame, text="Save & Encrypt", bg=ACCENT_COLOR, fg="white", width=14, relief="raised",
              command=lambda: handle_setup(mongo_entry, root)).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancel", bg=CANCEL_COLOR, fg="white", width=14, relief="raised",
              command=root.destroy).pack(side="left", padx=10)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()
