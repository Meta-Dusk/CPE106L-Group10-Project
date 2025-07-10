import flet as ft

image_sources = {
    "chaewon_stare" : "https://image.koreaboo.com/2025/04/Header-Image-2025-04-08T171312.835.jpg",
    "chaewon_side"  : "https://koreajoongangdaily.joins.com/data/photo/2022/04/07/3e7dd04f-cadc-4336-9577-95a96e153801.jpg",
    "chaewon_sad"   : "https://i.pinimg.com/736x/33/63/84/336384d11ac51be54c6b6b64cb93ff7e.jpg"
}

def default_image():
    return ft.Image(
        src=image_sources["chaewon_stare"],
        width=150,
        height=150,
        border_radius=75,
        fit=ft.ImageFit.COVER,
        gapless_playback=True,
    )
