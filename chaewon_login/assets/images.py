import flet as ft
import random

from enum import Enum
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets" / "images"
ICON_PATH = Path(__file__).parent.parent / "assets" / "icons" / "chae.ico"

class Image:
    def __init__(self, filename: str, description: str):
        self.filename = filename
        self.description = description

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
        description="Chaewon staring at you")
    CHAEWON_SIDE = Image(
        filename="chae_side.jpg",
        description="Chaewon looking at you")
    CHAEWON_SAD = Image(
        filename="chae_sad.jpg",
        description="Chaewon is sad 😔 because MongoDB is not connected")

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
    width: ft.OptionalNumber = 150,
    height: ft.OptionalNumber = 150,
    border_radius: ft.OptionalNumber = 0,
    fit: ft.ImageFit = ft.ImageFit.COVER,
    gapless_playback: bool = True,
    tooltip: str = None,
    error_content=error_content
) -> ft.Image:
    if ref is not None and isinstance(ref, ImageData):
        src = ref.value.path
        tooltip = ref.value.description
    return ft.Image(
        src=src,
        width=width,
        height=height,
        border_radius=border_radius,
        fit=fit,
        gapless_playback=gapless_playback,
        tooltip=tooltip,
        error_content=error_content
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
        width=random_width,
        height=random_height
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