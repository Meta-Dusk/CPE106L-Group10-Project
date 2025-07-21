import time
import flet as ft

def animate_fade_out(control: ft.Control, duration: float = 0.2):
    control.opacity = 0.0
    control.scale = 0.8
    control.update()
    time.sleep(duration)

def animate_fade_in(control: ft.Control, duration: float = 0.3, scale: float = 1.2, rotate: float = 0.15):
    control.opacity = 1.0
    control.scale = scale
    control.rotate = rotate
    control.update()
    time.sleep(duration)

def animate_reset(control: ft.Control):
    control.scale = 1.0
    control.rotate = 0.0
    control.update()

def container_setup(
    content: ft.Control | None = None
) -> ft.Control:
    return ft.Container(
        content=content,
        animate_opacity=300,
        animate_scale=500,
        animate_rotation=500,
        opacity=1.0,
        rotate=0.0,
        alignment=ft.alignment.center,
    )