# ffpl.py
# ---------

import os
import gc
import subprocess
from functools import lru_cache


class ffpl:
    """
    >>> CLASS FOR INTERFACING TO PLAY MULTIMEDIA FILES.

    ATTRIBUTES:
    ----------
    >>> -FFPL_PATH : STR
        >>> PATH TO THE FFPL EXECUTABLE.

    METHODS:
    -------
    >>> -PLAY(MEDIA_FILE)
        >>> PLAY MULTIMEDIA FILE.
    >>> EXAMPLE

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >>> from MediaSwift import ffpl
    >>> play = ffpl()
    >>> media_file = r"PATH_TO_MEDIA_FILE"
    >>> play.play(media_file)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ```
    >>> RETURNS: NONE
    """

    def __init__(self):
        """
        >>> INITIALIZE THE FFPL INSTANCE.
        >>> SETS THE DEFAULT PATH TO THE FFPL EXECUTABLE.

        >>> EXAMPLE

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpl

        >>> play = ffpl()
        >>> media_file = r"PATH_TO_MEDIA_FILE"
        >>> play.play(media_file)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURN: NONE
        """
        self.ffplay_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffpl.exe"
        )

    @lru_cache(maxsize=None)  # SETTING MAXSIZE TO NONE MEANS AN UNBOUNDED CACHE
    def play(self, media_file):
        """
        >>> PLAY MULTIMEDIA FILE USING FFPL WITH SPECIFIED VIDEO FILTERS.

        PARAMETERS:
        ------------
        >>> -MEDIA_FILE : STR
           >>> PATH TO THE MULTIMEDIA FILE TO BE PLAYED.

        >>> EXAMPLE

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpl

        >>> play = ffpl()
        >>> media_file = r"PATH_TO_MEDIA_FILE"
        >>> play.play(media_file)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURNS: NONE
        """
        # MODIFY THE COMMAND TO INCLUDE THE OPTIONS FOR SETTING
        command = [
            self.ffplay_path,
            "-hide_banner",
            "-fs",  # FULLSCREEN MODE
            "-vf",  # VIDEO FILTER OPTIONS
            "hqdn3d, unsharp",
            media_file,
        ]  # "-loglevel", "panic",  # ADD THIS LINE

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"FFPL COMMAND FAILED WITH ERROR: {e}")
        except Exception as e:
            print(f"AN ERROR OCCURRED: {e}")
        finally:
            gc.collect()
