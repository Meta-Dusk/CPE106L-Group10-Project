import flet as ft
import asyncio

from app.utils import milliseconds_to_seconds


async def text_pand(text: ft.Text, duration_in_milliseconds: int = 500):
    weights = [
        ft.FontWeight.W_100, ft.FontWeight.W_200, ft.FontWeight.W_300,
        ft.FontWeight.W_400, ft.FontWeight.W_500, ft.FontWeight.W_600,
        ft.FontWeight.W_700, ft.FontWeight.W_800, ft.FontWeight.W_900
    ]
    step_delay = milliseconds_to_seconds(duration_in_milliseconds / len(weights))

    for weight in weights:
        text.weight = weight
        text.update()
        await asyncio.sleep(step_delay)

async def animate_fade_in(control: ft.Control, duration_in_milliseconds: int = 500):
    control.animate_opacity = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_OUT)
    control.opacity = 1.0
    control.update()
    
    await asyncio.sleep(milliseconds_to_seconds(duration_in_milliseconds))

async def animate_fade_out(control: ft.Control, duration_in_milliseconds: int = 500):
    control.animate_opacity = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_OUT)
    control.opacity = 0.0
    control.update()
    
    await asyncio.sleep(milliseconds_to_seconds(duration_in_milliseconds))

# Fade out and slide right
async def animate_slide_out(control: ft.Control, duration_in_milliseconds: int = 500):
    control.animate_offset = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_CUBIC)
    control.animate_opacity = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_CUBIC)
    control.animate_rotation = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_OUT)
    control.offset = ft.Offset(1.0, 0.0)
    control.opacity = 0.0
    control.rotate = ft.Rotate(-0.05, ft.alignment.bottom_left)
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
    control.animate_offset = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_CUBIC)
    control.animate_opacity = ft.Animation(duration=duration_in_milliseconds, curve=ft.AnimationCurve.EASE_IN_CUBIC)
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
    control.offset = ft.Offset(0.0, 0.0)
    control.rotate = ft.Rotate(0.05, ft.alignment.bottom_right)
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
        animate_opacity=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT),
        animate_offset=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT),
        animate_rotation=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT),
        opacity=1.0,
        offset=ft.Offset(0, 0),
        rotate=0,
        alignment=ft.alignment.center
    )
