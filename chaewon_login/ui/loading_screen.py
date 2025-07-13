import flet as ft

"""
Try to import TEXT_LABEL_SIZE from constants; if it fails, use a default value.
Run loading_screen.py to test the loading screen UI.
"""
try:
    from constants import TEXT_LABEL_SIZE
except (ImportError, ModuleNotFoundError, AttributeError):
    TEXT_LABEL_SIZE = 25  # Fallback value

def show_loading_screen(page: ft.Page, message: str = "Connecting..."):
    loading_text = ft.Text(message, size=TEXT_LABEL_SIZE)
    loading_spinner = ft.ProgressRing()

    loading_ui = ft.Column(
        [loading_spinner, loading_text],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
    )

    page.add(ft.Container(content=loading_ui, alignment=ft.alignment.center, expand=True))
    page.update()


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
