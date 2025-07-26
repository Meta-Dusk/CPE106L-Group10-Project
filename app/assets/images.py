import flet as ft
import random

from enum import Enum
from pathlib import Path
from app.ui.theme_service import load_theme_mode
from typing import Optional


ASSETS_DIR = Path(__file__).parent.parent / "assets" / "images"
ICON_PATH = Path(__file__).parent.parent / "assets" / "icons" / "app.ico"

class Image:
    def __init__(
        self, filename: str, description: str,
        width: Optional[int] = 150, height: Optional[int] = 150
    ):
        self.filename = filename
        self.description = description
        self.width = width
        self.height = height

    def __str__(self):
        return f"{self.description ({self.path})}"
    
    @property
    def path(self) -> str:
        return f"images/{self.filename}"

    @property
    def file_path(self) -> Path:
        return ASSETS_DIR / self.filename

class ImageData(Enum):
    CHAEWON_STARE = Image(
        filename="chae_stare.jpg",
        description="Chaewon staring at you"
    )
    CHAEWON_SIDE = Image(
        filename="chae_side.jpg",
        description="Chaewon looking at you"
    )
    CHAEWON_SAD = Image(
        filename="chae_sad.jpg",
        description="Chaewon is sad 😔 because MongoDB is not connected"
    )
    LOGO_DARK = Image(
        filename="logo_dark.png",
        description="Project ATS(Accessible Transportation Scheduler) Logo but dark",
        width=404, height=167
    )
    LOGO_LIGHT = Image(
        filename="logo_light.png",
        description="Project ATS(Accessible Transportation Scheduler) Logo but light",
        width=404, height=167
    )
    METADUSK = Image(
        filename="brand.png",
        description="MetaDusk brand logo",
        width=355, height=265
    )

error_content = ft.Container(
    ft.Text(
        value="IMAGE_ERROR",
        color=ft.Colors.ON_ERROR,
        text_align=ft.TextAlign.CENTER
    ),
    bgcolor=ft.Colors.ERROR,
    alignment=ft.alignment.center,
    adaptive=True
)
    
def build_image(
    ref: ImageData = None,
    src: str = None,
    set_width: ft.OptionalNumber = None,
    set_height: ft.OptionalNumber = None,
    border_radius: ft.OptionalNumber = 0,
    fit: ft.ImageFit = ft.ImageFit.COVER,
    gapless_playback: bool = True,
    tooltip: str = None,
    error_content=error_content,
    color: ft.ColorValue = None,
    visible: bool = True,
    relative_width: ft.OptionalNumber = None,
    relative_height: ft.OptionalNumber = None,
    relative_scale: ft.OptionalNumber = None
) -> ft.Image:
    if ref is not None and isinstance(ref, ImageData):
        src = ref.value.path
        tooltip = ref.value.description

        # Use base width and height from ref if not manually overridden
        base_width = ref.value.width
        base_height = ref.value.height

        if relative_scale is not None:
            set_width = base_width * relative_scale
            set_height = base_height * relative_scale
        else:
            if relative_width is not None:
                set_width = base_width * relative_width
            if relative_height is not None:
                set_height = base_height * relative_height
                
    return ft.Image(
        src=src,
        width=set_width,
        height=set_height,
        border_radius=border_radius,
        fit=fit,
        gapless_playback=gapless_playback,
        tooltip=tooltip,
        error_content=error_content,
        color=color,
        visible=visible
    )
    
def generate_random_image() -> ft.Image:
    if not list(ImageData):
        return default_image()
    random_ref = random.choice(list(ImageData))
    random_border_radius = random.randint(0, 100)
    random_width = random.randint(150, 300)
    random_height = random.randint(150, 300)
    return build_image(
        ref=random_ref,
        border_radius=random_border_radius,
        set_width=random_width,
        set_height=random_height
    )
    
def update_image_with_random(img: ft.Image):
    new_img = generate_random_image()
    img.src = new_img.src
    img.tooltip = new_img.tooltip
    img.semantics_label = new_img.semantics_label
    img.border_radius = new_img.border_radius
    img.width = new_img.width
    img.height = new_img.height
    img.update()
    
def default_image() -> ft.Image:
    return build_image(ref=ImageData.CHAEWON_STARE, border_radius=75)

def set_logo(src: str = None) -> ft.Image:
    if src is None:
        if load_theme_mode == ft.ThemeMode.DARK:
            src = ImageData.LOGO_LIGHT.value.path
        else:
            src = ImageData.LOGO_DARK.value.path
    return build_image(src=src, color=ft.Colors.PRIMARY)


""" Run images.py to test the image data and to check the available images. """

def test():
    print("\nThe following are the available images:\n")
    for image in ImageData:
        img = image.value
        file_path = img.file_path
        exists = "✅ Found" if file_path.exists() else "❌ Missing"
        print(f"🖼️  \"{image.name}\"\t : {image.value.description}")
        print(f"   - Web path\t\t: {image.value.path}")
        print(f"   - File path\t\t: {file_path} ({exists})\n")

    
if __name__ == "__main__":
    test()