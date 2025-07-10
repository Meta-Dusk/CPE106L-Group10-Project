import flet as ft
from enum import Enum

class Image:
    def __init__(self, url: str, description: str):
        self.url = url
        self.description = description

    def __str__(self):
        return f"{self.description} ({self.url})"

class ImageData(Enum):
    CHAEWON_STARE = Image(
        "https://image.koreaboo.com/2025/04/Header-Image-2025-04-08T171312.835.jpg",
        "Chaewon staring at you"
    )
    CHAEWON_SIDE = Image(
        "https://koreajoongangdaily.joins.com/data/photo/2022/04/07/3e7dd04f-cadc-4336-9577-95a96e153801.jpg",
        "Chaewon looking at you"
    )
    CHAEWON_SAD = Image(
        "https://i.pinimg.com/736x/33/63/84/336384d11ac51be54c6b6b64cb93ff7e.jpg",
        "Chaewon is sad 😔 because MongoDB is not connected"
    )

def default_image():
    return ft.Image(
        src=ImageData.CHAEWON_STARE.value.url,
        width=150,
        height=150,
        border_radius=75,
        fit=ft.ImageFit.COVER,
        gapless_playback=True,
        tooltip=ImageData.CHAEWON_STARE.value.description,
    )

def main():
    print("The following are the available images:")
    for image in ImageData:
        print(f"\"{image.name}\", Description: \"{image.value.description}\", from: {image.value.url}")
    
if __name__ == "__main__":
    main()