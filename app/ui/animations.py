import flet as ft
import asyncio

from app.utils import milliseconds_to_seconds


# Fade out and slide right
async def animated_slide_out(control: ft.Control, duration_in_milliseconds: int = 500):
    control.animate_offset = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_CUBIC)
    control.animate_opacity = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_CUBIC)
    control.animate_rotation = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_OUT_QUART)
    control.offset = ft.Offset(1.0, 0.25)
    control.opacity = 0.0
    control.rotate = ft.Rotate(-0.2, ft.alignment.bottom_left)
    control.update()

    # Wait for fade out to complete
    await asyncio.sleep(milliseconds_to_seconds(duration_in_milliseconds))

# Move instantly to left, no animation
async def prepare_for_slide_in(control: ft.Control):
    # Disable animation
    control.animate_offset = ft.Animation(duration=0)
    
    # Set origin points
    control.offset = ft.Offset(-1.0, -0.2)
    control.update()
    await asyncio.sleep(0.01)  # Let the update apply

# Fade in and slide to center
async def animate_slide_in(control: ft.Control, duration_in_milliseconds: int = 500):
    control.animate_offset = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT)
    control.animate_opacity = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT)
    control.animate_rotation = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.LINEAR)
    control.opacity = 1.0
    control.offset = ft.Offset(0, 0)
    control.rotate = 0.0
    control.update()
    await asyncio.sleep(milliseconds_to_seconds(duration_in_milliseconds))

# Rotate a bit to the right
async def teeter_right(control: ft.Control, duration_in_milliseconds: int = 200):
    control.animate_offset = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_OUT_CUBIC)
    control.animate_rotation = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_OUT)
    control.offset = ft.Offset(0.0, 0.15)
    control.rotate = ft.Rotate(0.1, ft.alignment.bottom_right)
    control.update()
    await asyncio.sleep(milliseconds_to_seconds(duration_in_milliseconds/2))
    control.offset = ft.Offset(0.0, 0.0)
    control.rotate = ft.Rotate(0.0, ft.alignment.bottom_right)
    control.update()
    await asyncio.sleep(milliseconds_to_seconds(duration_in_milliseconds/2))

# Reset scale and rotation
async def animate_reset(control: ft.Control):
    control.scale = 1.0
    control.rotate = 0.0
    control.offset = ft.Offset(0.0, 0.0)
    control.update()

def container_setup(content: ft.Control | None = None) -> ft.Container:
    return ft.Container(
        content=content,
        animate_opacity=500,
        animate_offset=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT),
        animate_rotation=500,
        opacity=1.0,
        offset=ft.Offset(0, 0),
        rotate=0,
        alignment=ft.alignment.center,
    )
