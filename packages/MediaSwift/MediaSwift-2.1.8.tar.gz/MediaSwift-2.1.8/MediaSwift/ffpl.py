# ffpl.py
# ---------

from rich.console import Console
import os
import gc
import subprocess
from functools import lru_cache
import time
import threading

console = Console()


class ffpl:
    """
    >>> CLASS FOR INTERFACING TO PLAY MULTIMEDIA FILES.

    ATTRIBUTES
    ----------
    >>> ↠ FFPL_PATH : STR
        >>> PATH TO THE FFPL EXECUTABLE.

    METHODS
    -------
    >>> ↠ PLAY(MEDIA_FILE)
        >>> PLAY MULTIMEDIA FILE.
    >>> EXAMPLE:

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

        >>> EXAMPLE:

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

        ↠ PARAMETER'S
        ------------
        >>> MEDIA_FILE : STR
           >>> PATH TO THE MULTIMEDIA FILE TO BE PLAYED.

        >>> EXAMPLE:

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
        # MODIFY THE COMMAND TO INCLUDE THE OPTIONS FOR SETTING.

        command = [
            self.ffplay_path,
            "-hide_banner",
            "-fs",
            "-vf",
            "hqdn3d, unsharp",
            "-loglevel",
            "panic",
            media_file,
        ]

        console.print("MUSIC PLAYING 🎵 \n", style="bold green")

        # PRINT A CYCLIC WAVE PATTERN TO CREATE AN ILLUSION OF A MOVING WAVE.
        def print_wave_pattern(stop_wave_pattern):
            wave_pattern = "⣀⣀⣀⣤⣤⣤⣶⣶⣶⣿⣿⣿⣿⣿⣿⣶⣶⣶⣤⣤⣤⣀⣀⣀"
            while not stop_wave_pattern.is_set():
                console.print(wave_pattern, end="\r", style="bold cyan")
                wave_pattern = wave_pattern[2:] + wave_pattern[:2]
                time.sleep(0.1)

        # CREATE AN EVENT TO SIGNAL THE THREAD TO STOP.
        stop_wave_pattern = threading.Event()

        # START A SEPARATE THREAD TO PRINT THE WAVE PATTERN.
        wave_thread = threading.Thread(
            target=print_wave_pattern, args=(stop_wave_pattern,)
        )
        wave_thread.daemon = True  # SET THE THREAD AS A DAEMON THREAD.
        wave_thread.start()

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            console.print(
                f"AN ERROR OCCURRED WHILE PLAYING THE MEDIA FILE: {e}", style="bold red"
            )
        except Exception as e:
            console.print(f"AN UNEXPECTED ERROR OCCURRED: {e}", style="bold red")
        finally:
            # SIGNAL THE WAVE PATTERN THREAD TO STOP GRACEFULLY.
            stop_wave_pattern.set()
            wave_thread.join()  # WAIT FOR THE THREAD TO COMPLETE.

            os.system("cls")
            console.print("MUSIC PLAYER EXITED..", style="bold yellow")
            time.sleep(2)
            os.system("cls")
            gc.collect()
