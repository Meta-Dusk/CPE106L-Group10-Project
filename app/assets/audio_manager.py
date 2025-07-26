import pygame
import threading
import time
import random

from pathlib import Path
from enum import Enum
from typing import Callable, List, Dict


ASSETS_DIR = Path(__file__).parent / "sounds"
SFX_DIR = ASSETS_DIR / "sfx"
BGM_DIR = ASSETS_DIR / "music"

# TODO: Try to implement flet-audio as an alternative when app is run in a web environment
def run_in_background(func):
    """Decorator to run a function in a background daemon thread."""
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper

class SFX(Enum):
    CLICK = "01-mouse_click.wav"
    NOTIF = "back_style_1_echo_007.wav"
    ALERT = "back_style_2_echo_007.wav"
    ERROR = "error_style_2_001.wav"
    DB = "back_style_5_echo_007.wav"
    THEME = "back_style_5_echo_007.wav"
    EXIT = "confirm_style_6_004.wav"
    REWARD = "confirm_style_4_echo_005.wav"

class BGM(Enum):
    GYMNOPEDIE = "satie_gymnopedie-no-1.mp3"
    BACH_G_STRING = "bach_air-on-the-g-string.mp3"
    NOCTURNE_N20_CSM = "chopin_nocturne-no-20-in-c-sharp-minor.mp3"
    SWAN_LAKE = "tchaikovsky_swan-lake.mp3"
    ARABESQUE = "debussy_arabesque-no-1.mp3"
    CONSOLATION = "liszt_consolation-no-3.mp3"
    REVERIE = "debussy_reverie.mp3"

class AudioManager:
    def __init__(self):
        self.sfx = {}
        self.bgm = {}
        self.current_bgm = None
        self._muted = False
        self._ready = False
        self._on_ready_callbacks: List[Callable[[], None]] = []
        self.limit_sfx_rate = False  # Toggle to enable/disable SFX rate limiting
        self._sfx_last_played: Dict[str, float] = {}  # Tracks last play time per SFX
        self._sfx_min_interval = 0.1  # Minimum interval (in seconds) between plays of same SFX

    def init(self):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
                print("[AudioManager] Audio initialized.")
            except pygame.error as e:
                print(f"[AudioManager] Failed to initialize audio: {e}")
                return
        else:
            print("[AudioManager] Audio already initialized!")
            
        self._load_all_sounds()
        self._ready = True
        print("[AudioManager] AudioManager is ready.")
        self._trigger_callbacks()

    def _trigger_callbacks(self):
        for callback in self._on_ready_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"[AudioManager] Callback error: {e}")
        self._on_ready_callbacks.clear()

    def on_ready(self, callback: Callable[[], None]):
        """Register a function to be called when audio is ready."""
        if self._ready:
            callback()
        else:
            self._on_ready_callbacks.append(callback)

    def _load_all_sounds(self):
        for file in SFX_DIR.glob("*.wav"):
            self.sfx[file.name] = pygame.mixer.Sound(file.as_posix())
        for file in BGM_DIR.glob("*.mp3"):
            self.bgm[file.name] = file

    def _clamp_volume(self, volume: float) -> float:
        if not 0.0 <= volume <= 1.0:
            print(f"[AudioManager] Provided volume is out of acceptable range: {volume}")
            print("Volume will be capped between 0.0 and 1.0")
        return max(0.0, min(volume, 1.0))

    def set_sfx_rate_limit(self, interval_sec: float):
        self._sfx_min_interval = max(0.01, interval_sec) # Avoid zero or negative
    
    def play_sfx(self, sfx_enum: SFX, volume: float = 0.5):
        if not self.can_play:
            return
        
        now = time.time()
        sfx_key = sfx_enum.value
        
        if self.limit_sfx_rate:
            last_played = self._sfx_last_played.get(sfx_key, 0)
            if now - last_played < self._sfx_min_interval:
                return # Skip playback if too soon
        
        sound = self.sfx.get(sfx_key)
        if sound:
            sound.set_volume(self._clamp_volume(volume))
            sound.play()
            self._sfx_last_played[sfx_key] = now # Update last played time
    
    def play_bgm(self, bgm_enum: BGM, volume: float = 0.5, loops: int = -1):
        if not self.can_play:
            return
        if self.current_bgm != bgm_enum.value:
            bgm_path = self.bgm[bgm_enum.value]
            file_name = bgm_path.name
            formatted_name = self.format_bgm_name(file_name)
            print(f"🎵 Now Playing 🎵 | {formatted_name}")
            pygame.mixer.music.load(bgm_path.as_posix())
            pygame.mixer.music.set_volume(self._clamp_volume(volume))
            pygame.mixer.music.play(loops)
            self.current_bgm = bgm_enum.value

    def play_random_bgm(self, bgm_enums: list[BGM] = None, volume: float = 0.5, loops: int = -1):
        if not self.can_play:
            return
        
        # Use provided list or fall back to all BGMs
        bgm_list = bgm_enums if bgm_enums else list(BGM)
        random_bgm = random.choice(bgm_list)
        
        # Play only if it's not already playing
        if self.current_bgm != random_bgm:
            self.play_bgm(random_bgm, volume=volume, loops=loops)
    
    def stop_bgm(self):
        pygame.mixer.music.stop()
        self.current_bgm = None

    def mute(self):
        self._muted = not self._muted
        if self._muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    @property
    def muted(self):
        return self._muted
    
    @property
    def can_play(self) -> bool:
        return self._ready and not self._muted
    
    @staticmethod
    def format_bgm_name(file_name: str) -> str:
        # Remove file extension
        base_name = file_name.removesuffix(".mp3")
        
        # Split into author and title
        if "_" in base_name:
            author_part, title_part = base_name.split("_", 1)
        else:
            author_part, title_part = "Unknown", base_name  # Fallback
        
        # Format parts
        author = author_part.capitalize()
        title = title_part.replace("-", " ").title()
        
        return f"{title} by {author}"


# Shared global instance
audio = AudioManager()

@run_in_background
def setup_audio():
    audio.init()
