import asyncio
import flet as ft


class SplashHandler:
    def __init__(self, page: ft.Page):
        self.page = page
        self.skip_event = asyncio.Event()
        self.skip_triggered = False
        self.active = True  # Use this to disable future delays after cleanup

    def on_skip_event(self, e: ft.KeyboardEvent):
        if not self.skip_triggered:
            self.skip_triggered = True
            self.skip_event.set()

    def cleanup(self):
        self.active = False
        self.page.controls.clear()
        self.page.on_keyboard_event = None
        self.page.update()

    async def skippable_delay(self, seconds: float) -> bool:
        if not self.active:
            return False
        try:
            await asyncio.wait_for(self.skip_event.wait(), timeout=seconds)
        except asyncio.TimeoutError:
            return True  # not skipped, delay finished
        self.cleanup()
        return False     # was skipped

    async def force_skip(self):
        self.skip_triggered = True
        self.skip_event.set()
        self.cleanup()
        
    def skippable_animation(self, auto_cleanup: bool = True):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                animation_task = asyncio.create_task(func(*args, **kwargs))
                skip_task = asyncio.create_task(self.skip_event.wait())

                done, _ = await asyncio.wait(
                    [animation_task, skip_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                if skip_task in done:
                    animation_task.cancel()
                    if auto_cleanup:
                        self.cleanup()
                    return False
                else:
                    skip_task.cancel()
                    if auto_cleanup:
                        self.cleanup()
                    return True
            return wrapper
        return decorator
    
    # == Decorators ==
    def auto_cleanup(self):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    if self.active:
                        self.cleanup()
            return wrapper
        return decorator
