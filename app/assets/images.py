import flet as ft
import random

from enum import Enum
from pathlib import Path
from app.ui.services.theme_service import load_theme_mode
from typing import Optional, Sequence, Tuple


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
    ICON_DARK = Image(
        filename="icon_dark.png",
        description="App Icon but dark",
        width=500, height=369
    )
    ICON_LIGHT = Image(
        filename="icon_light.png",
        description="App Icon but light",
        width=500, height=369
    )
    ANDREI = Image(
        filename="andrei.png",
        description="John Andrei M. Dela Cruz"
    )
    NIGEL = Image(
        filename="nigel.jpg",
        description="Vicente Nigel S. Dayag Jr."
    )
    SETH = Image(
        filename="seth.jpg",
        description="John Seth B. Regalado"
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

# == Bum ass CircleAvatar; it just doesn't work...
# def build_avatar(
#     ref: ImageData = None,
#     initials: Optional[str] = None,
#     color: ft.ColorValue = ft.Colors.PRIMARY,
#     bgcolor: ft.ColorValue = ft.Colors.SECONDARY,
#     set_width: ft.OptionalNumber = None,
#     set_height: ft.OptionalNumber = None,
#     set_size: ft.OptionalNumber = 100,
#     visible: bool = True,
#     relative_width: ft.OptionalNumber = None,
#     relative_height: ft.OptionalNumber = None,
#     relative_scale: ft.OptionalNumber = None,
#     tooltip: Optional[str] = None
# ) -> ft.CircleAvatar:
#     if ref is not None:
#         foreground_image_src = ref.value.path
#         tooltip = ref.value.description if tooltip is None else tooltip
#         base_width = ref.value.width
#         base_height = ref.value.height
#     else:
#         foreground_image_src = None
#         base_width = 200
#         base_height = 200

#     # Relative scaling
#     if relative_scale is not None:
#         set_width = base_width * relative_scale
#         set_height = base_height * relative_scale
#     else:
#         if relative_width is not None:
#             set_width = base_width * relative_width
#         if relative_height is not None:
#             set_height = base_height * relative_height
    
#     # Absolute sizing overrides relative scaling
#     if set_size is not None:
#         set_width = set_size
#         set_height = set_size
    
#     content = ft.Text(value=initials) if initials else None
    
#     return ft.CircleAvatar(
#         content=content,
#         foreground_image_src=foreground_image_src,
#         tooltip=tooltip,
#         # color=color,
#         # bgcolor=bgcolor,
#         width=set_width,
#         height=set_height,
#         visible=visible
#     )
    
def build_image(
    ref: ImageData = None,
    src: str = None,
    set_width: ft.OptionalNumber = None,
    set_height: ft.OptionalNumber = None,
    set_size: ft.OptionalNumber = None,
    border_radius: ft.OptionalNumber = 0,
    fit: ft.ImageFit = ft.ImageFit.COVER,
    gapless_playback: bool = True,
    tooltip: str = None,
    error_content=error_content,
    color: ft.ColorValue = None,
    visible: bool = True,
    relative_width: ft.OptionalNumber = None,
    relative_height: ft.OptionalNumber = None,
    relative_scale: ft.OptionalNumber = None,
) -> ft.Image:
    base_width, base_height = None, None

    if ref is not None and isinstance(ref, ImageData):
        src = ref.value.path
        tooltip = tooltip or ref.value.description
        base_width = ref.value.width
        base_height = ref.value.height
    elif src:
        tooltip = tooltip or "Image"  # fallback tooltip
        base_width, base_height = 200, 200  # fallback base size

    # Apply scaling if base size is known
    if base_width and base_height:
        if relative_scale is not None:
            set_width = base_width * relative_scale
            set_height = base_height * relative_scale
        else:
            if relative_width is not None:
                set_width = base_width * relative_width
            if relative_height is not None:
                set_height = base_height * relative_height

    # Absolute sizing overrides everything else
    if set_size is not None:
        set_width = set_size
        set_height = set_size

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
    
def generate_random_image(
    src: Optional[Sequence[ImageData]] = None,
    random_width: Tuple[int, int] = (150, 300),
    random_height: Tuple[int, int] = (150, 300),
    random_border_radius: Tuple[int, int] = (150, 300),
) -> ft.Image:
    """
    Generates a random image based on a provided list.
    Defaults to all current images defined in `ImageData`.

    Args:
        src (Sequence[ImageData], optional): A list of `ImageData` items.  If None, uses all defined ImageData enum values.
        random_width (Tuple[int, int], optional): Min and max range for width.
        random_height (Tuple[int, int], optional): Min and max range for height.
        random_border_radius (Tuple[int, int], optional): Min and max range for border radius.

    Returns:
        ft.Image: A randomly built image with random size and border radius.
    """
    if not src:
        src = list(ImageData)
    
    set_random_ref = random.choice(src)
    set_random_border_radius = random.randint(*random_border_radius)
    set_random_width = random.randint(*random_width)
    set_random_height = random.randint(*random_height)
    
    return build_image(
        ref=set_random_ref,
        border_radius=set_random_border_radius,
        set_width=set_random_width,
        set_height=set_random_height
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

def set_logo(
    src: Optional[ImageData] = None,
    relative_scale: ft.OptionalNumber = 0.9,
    tooltip: Optional[str] = "",
    color: ft.ColorValue = ft.Colors.PRIMARY
) -> ft.Image:
    """
    Builds a logo image based on the current theme mode.

    Args:
        src (Optional[ImageData]): Optional image override. Defaults to a theme-based logo.
        relative_scale (float): Scaling multiplier for logo size.
        tooltip (str): Tooltip text shown on hover.

    Returns:
        ft.Image: The configured image component.
    """
    # Theme-based fallback logo
    if src is None:
        src = ImageData.LOGO_DARK if load_theme_mode == ft.ThemeMode.LIGHT else ImageData.LOGO_LIGHT
    elif src in (ImageData.ICON_DARK, ImageData.ICON_LIGHT):
        color = None
        # Theme-based fallback for icons
        src = ImageData.ICON_DARK if load_theme_mode == ft.ThemeMode.LIGHT else ImageData.ICON_LIGHT

    return build_image(
        ref=src,
        color=color,
        relative_scale=relative_scale,
        tooltip=tooltip,
    )


"""
Run images.py to test the image data and to check the available images.
Run with:
py -m app.assets.images
"""

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