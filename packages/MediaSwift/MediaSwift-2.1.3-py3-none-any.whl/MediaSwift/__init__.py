# __init__.py
# -------------

from .ffpe import ffpe
from .ffpr import ffpr
from .ffpl import ffpl

__all__ = ["ffpe", "ffpr", "ffpl", "version"]

__version__ = "2.1.1"


def version():
    return "LIBRARY VERSION: " + __version__


import os


def add_ffmpeg_to_path():
    ffmpeg_path = os.path.join(os.path.dirname(__file__), "..", "bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path


add_ffmpeg_to_path()
