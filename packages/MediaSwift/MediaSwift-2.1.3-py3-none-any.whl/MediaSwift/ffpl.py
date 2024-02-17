# ffpl.py
# ---------

import os
import gc
import subprocess
from functools import lru_cache


class ffpl:
    """
    >>> CLASS FOR INTERFACING WITH FFPLAY TO PLAY MULTIMEDIA FILES.

    ATTRIBUTES
    ----------
    >>> FFPLAY_PATH : STR

        >>> PATH TO THE FFPLAY EXECUTABLE.

    METHODS
    -------
    >>> PLAY(MEDIA_FILE)

        >>> PLAY MULTIMEDIA FILE USING FFPLAY WITH SPECIFIED VIDEO FILTERS.
    >>> EXAMPLE

    ```python
    =================================================================
    >>> from MediaSwiftPy import ffpl
    >>> play = ffpl()
    >>> media_file = r"PATH_TO_MEDIA_FILE"
    >>> play.play(media_file)
    =================================================================

    ```
    >>> RETURNS: NONE
    """

    def __init__(self):
        """
        >>> INITIALIZE THE FFPL INSTANCE.

        >>> SETS THE DEFAULT PATH TO THE FFPLAY EXECUTABLE.

        >>> EXAMPLE

        ```python
        =================================================================
        >>> from MediaSwiftPy import ffpl

        >>> play = ffpl()
        >>> media_file = r"PATH_TO_MEDIA_FILE"
        >>> play.play(media_file)
        =================================================================
        ```
        >>> RETURN: NONE
        """
        self.ffplay_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffplay.exe"
        )

    @lru_cache(maxsize=None)  # SETTING MAXSIZE TO NONE MEANS AN UNBOUNDED CACHE
    def play(self, media_file):
        """
        >>> PLAY MULTIMEDIA FILE USING FFPLAY WITH SPECIFIED VIDEO FILTERS.

        PARAMETERS
        ------------
        >>> MEDIA_FILE : STR
           >>> PATH TO THE MULTIMEDIA FILE TO BE PLAYED.

        >>> RETURNS: NONE
        """
        # MODIFY THE COMMAND TO INCLUDE THE OPTIONS FOR SETTING THE AUDIO SAMPLE RATE TO 48000 HZ
        command = [
            self.ffplay_path,
            "-hide_banner",
            "-fs",  # FULLSCREEN MODE
            "-vf",  # VIDEO FILTER OPTIONS
            "hqdn3d, unsharp",
            media_file,
        ]  # "-loglevel", "panic",  # Add this line

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"FFplay command failed with error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            gc.collect()
