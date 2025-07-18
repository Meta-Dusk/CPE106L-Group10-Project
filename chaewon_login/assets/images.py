import flet as ft

from enum import Enum
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets" / "images"
ICON_PATH = Path(__file__).parent.parent / "assets" / "icons" / "chae.ico"

class Image:
    def __init__(self, filename: str, description: str):
        self.filename = filename
        self.description = description

    @property
    def path(self) -> str:
        return f"images/{self.filename}"

    @property
    def file_path(self) -> Path:
        return ASSETS_DIR

class ImageData(Enum):
    CHAEWON_STARE = Image(
        "chae_stare.jpg",
        "Chaewon staring at you"
    )
    CHAEWON_SIDE = Image(
        "chae_side.jpg",
        "Chaewon looking at you"
    )
    CHAEWON_SAD = Image(
        "chae_sad.jpg",
        "Chaewon is sad 😔 because MongoDB is not connected"
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

def default_image():
    return ft.Image(
        src=ImageData.CHAEWON_STARE.value.path,
        width=150,
        height=150,
        border_radius=75,
        fit=ft.ImageFit.COVER,
        gapless_playback=True,
        tooltip=ImageData.CHAEWON_STARE.value.description,
        error_content=error_content
    )

""" Run images.py to test the image data and to check the available images. """

def test():
    print("The following are the available images:\n")
    for image in ImageData:
        file_path = image.value.file_path
        exists = "✅ Found" if file_path.exists() else "❌ Missing"
        print(f"🖼️  \"{image.name}\": {image.value.description}")
        print(f"   - Web path: {image.value.path}")
        print(f"   - File path: {file_path} ({exists})\n")

    
if __name__ == "__main__":
    test()