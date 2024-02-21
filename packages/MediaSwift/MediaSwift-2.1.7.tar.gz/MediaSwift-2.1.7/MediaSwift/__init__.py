# __init__.py
# -------------

import os

from .ffpe import ffpe
from .ffpr import ffpr
from .ffpl import ffpl

__all__ = ["ffpe", "ffpr", "ffpl", "version"]

__version__ = "2.1.7"


def version():
    """
    >>> RETURNS THE LIBRARY VERSION.

    RETURN:
    -------
        >>> STR: THE LIBRARY VERSION.

    >>> EXAMPLE:

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    from MediaSwift import version

    info = version()
    print(info)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```
    >>> RETURN: NONE
    """
    return "LIBRARY VERSION: " + __version__


def add_ffmpeg_to_path():
    """
    >>> ADD THE LIBRARY'S FFMPEG BINARY PATH TO THE SYSTEM PATH.
    """
    ffmpeg_path = os.path.join(os.path.dirname(__file__), "..", "bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path


add_ffmpeg_to_path()
