from .voxscribe import (
    clean_up,
    get_text_from_base64,
    get_text_from_MP3,
    get_text_from_url,
    get_text_from_WAV,
)

__version__ = "1.1.2"
__all__ = [
    "clean_up",
    "get_text_from_base64",
    "get_text_from_MP3",
    "get_text_from_url",
    "get_text_from_WAV",
]
""" FFMPEG needs to be installed and in your PATH for this module to work. """
clean_up(max_age=5)
