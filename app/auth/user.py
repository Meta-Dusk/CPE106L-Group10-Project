import flet as ft

def is_authenticated(page: ft.Page) -> bool:
    return bool(page.session.get("user_authenticated"))

def logout_yes(
    page: ft.Page,
    dialog: ft.AlertDialog,
    page_destination: str
):
    page.close(dialog)
    page.session.clear()
    page.go(page_destination)
    page.update()

def logout_no(
    page: ft.Page,
    dialog: ft.AlertDialog
):
    page.close(dialog)
    page.update()

# def logout(page: ft.Page):
#     page.session.clear()
#     page.go(PageRoute.LOGIN.value)