import flet as ft

from chaewon_login.ui.components.containers import default_column, default_container
from chaewon_login.ui.components.text import default_text, TextType


def show_loading_screen(page: ft.Page, message: str = "Connecting..."):
    loading_text = default_text(TextType.TITLE, message)
    loading_spinner = ft.ProgressRing(width=200,height=200)

    loading_ui = default_column(controls=
        [
            loading_spinner,
            loading_text
        ]
    )

    page.add(default_container(loading_ui))
    page.update()


"""
Run loading_screen.py to test the loading screen UI.
Use the following command to run:
py -m chaewon_login.ui.loading_screen
"""

def test(page: ft.Page):
    show_loading_screen(page, "Loading application...")

    # Simulate some loading time
    import time
    import threading

    def remove_loading():
        time.sleep(2)
        page.controls.clear()
        page.update()
        print("Loading screen simulation finished.")

    threading.Thread(target=remove_loading).start()

if __name__ == "__main__":
    ft.app(target=test)
