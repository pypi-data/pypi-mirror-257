# ffpr.py
# ---------

import os
import json
import subprocess
from functools import lru_cache
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.text import Text

class FFProbeResult:
    """
    >>> REPRESENTS THE RESULT OF FFPROBE ANALYSIS ON A MULTIMEDIA FILE.

    ATTRIBUTES
    ----------
    >>> INFO : DICT
        >>> INFORMATION OBTAINED FROM FFPROBE.

    METHODS
    -------
    >>> DURATION() -> OPTIONAL[FLOAT]:
        >>> GET THE DURATION OF THE MULTIMEDIA FILE.
    >>> BIT_RATE() -> OPTIONAL[FLOAT]:
        >>> GET THE BIT RATE OF THE MULTIMEDIA FILE.
    >>> NB_STREAMS() -> OPTIONAL[INT]:
        >>> GET THE NUMBER OF STREAMS IN THE MULTIMEDIA FILE.
    STREAMS():
        >>> GET THE DETAILS OF INDIVIDUAL STREAMS IN THE MULTIMEDIA FILE.

        >>> EXAMPLE:


        ```python
        =================================================================
        >>> from MediaSWiftPy import ffpr

        >>> FFPROBE = ffpr()
        >>> INFO = FFPROBE.probe(r"PATH_TO_MEDIA_FILE")
        >>> FFPROBE.PRETTY(INFO)
        =================================================================
        ```

    >>> USE "PRETTY()" FOR MORE BEAUTIFY CONTENT SHOW.
    >>> RETURN NONE
    """

    def __init__(self, info):
        self.info = info

    @property
    def DURATION(self) -> Optional[float]:
        try:
            return float(self.info["format"]["duration"])
        except (KeyError, ValueError):
            return None

    @property
    def BIT_RATE(self) -> Optional[float]:
        try:
            return int(self.info["format"]["bit_rate"]) / 1000
        except (KeyError, ValueError):
            return None

    @property
    def NB_STREAMS(self) -> Optional[int]:
        return self.info["format"].get("nb_streams")

    @property
    def STREAMS(self):
        return self.info["streams"]


class ffpr:
    """
    >>> A CLASS FOR INTERFACING WITH FFPR TO ANALYZE MULTIMEDIA FILES.

    METHODS
    -------
    PROBE[INPUT_FILE] -> OPTIONAL:
    ---------------------------------------------
        >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.
    PRETTY(INFO):
    ----------------------------
        >>> PRINT READABLE SUMMARY OF THE FFPR ANALYSIS RESULT, MAKE BEAUTIFY CONTENT.

        >>> EXAMPLE:


        ```python
        =================================================================
        >>> from MediaSWiftPy import ffpr

        >>> DETAILS = ffpr()
        >>> INFO = DETAILS.probe(r"PATH_TO_MEDIA_FILE")
        >>> DETAILS.PRETTY(INFO)
        =================================================================
        ```

    >>> USE "PRETTY()" FOR MORE BEAUTIFY CONTENT SHOW.
    >>> RETURN: NONE
    """

    console = Console()  # Declare console at the class level

    def __init__(self):
        self._ffprobe_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffprobe.exe"
        )
        self.info = None

    @property
    def ffprobe_path(self):
        return self._ffprobe_path

    @lru_cache(maxsize=None)
    def probe(self, input_file) -> Optional[FFProbeResult]:
        """
        >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.

        PARAMETERS
        ----------
        INPUT_FILE : STR
        -----------------
            >>> PATH TO THE MULTIMEDIA FILE.

        OPTIONAL:
        ----------
            >>> RESULT OF THE FFPR ANALYSIS.
            >>> RETURN: NONE
        """
        try:
            command = [
                self.ffprobe_path,
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                input_file,
            ]
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            self.info = FFProbeResult(json.loads(result.stdout.decode("utf-8")))
            return self.info
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def pretty(self, info: FFProbeResult):
        """
        >>> PRINT READABLE SUMMARY OF THE FFPR ANALYSIS RESULT, MAKE BEAUTIFY CONTENT.

        PARAMETERS
        ----------
        INFO :
        -------
            >>> RESULT OF THE FFPR ANALYSIS.
            >>> RETURN: NONE
        """
        if not info:
            self.console.print("[bold magenta]NO INFORMATION AVAILABLE.[/bold magenta]")
            return

        self.console.print("\n[bold magenta]MEDIA FILE ANALYSIS SUMMARY[/bold magenta]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("[bold magenta]PROPERTY[/bold magenta]")
        table.add_column("[bold magenta]VALUE[/bold magenta]")

        table.add_row("[bold magenta]FILE[/bold magenta]", info.info["format"]["filename"])

        try:
            duration_seconds = info.DURATION
            minutes, seconds = divmod(duration_seconds, 60)
            table.add_row("[bold magenta]DURATION[/bold magenta]", f"{int(minutes)}:{int(seconds)} min")
        except (AttributeError, KeyError, ValueError):
            table.add_row("[bold magenta]DURATION[/bold magenta]", "N/A")

        try:
            bit_rate_kbps = info.BIT_RATE
            table.add_row("[bold magenta]BIT RATE[/bold magenta]", f"{bit_rate_kbps} kbit/s")
        except (AttributeError, KeyError, ValueError):
            table.add_row("[bold magenta]BIT RATE[/bold magenta]", "N/A")

        table.add_row("[bold magenta]NUMBER OF STREAMS[/bold magenta]", str(info.NB_STREAMS))

        self.console.print(table)

        for i, stream in enumerate(info.STREAMS):
            stream_type = stream.get("codec_type", "N/A")

            title = Text(f"{stream_type.capitalize()} STREAM {i + 1}", style="bold magenta")
            title.stylize("[underline]")

            self.console.print(title)

            sub_table = Table(show_header=True, header_style="bold magenta")
            sub_table.add_column("[bold magenta]ATTRIBUTE[/bold magenta]")
            sub_table.add_column("[bold magenta]VALUE[/bold magenta]")

            sub_table.add_row("[bold magenta]CODEC[/bold magenta]", str(stream.get("codec_name", "N/A")))
            sub_table.add_row("[bold magenta]PROFILE[/bold magenta]", str(stream.get("profile", "N/A")))

            try:
                bit_rate_kbps = int(stream.get("bit_rate", "N/A")) / 1000
                sub_table.add_row("[bold magenta]BIT RATE[/bold magenta]", f"{bit_rate_kbps} kbit/s")
            except (KeyError, ValueError):
                sub_table.add_row("[bold magenta]BIT RATE[/bold magenta]", "N/A")

            sub_table.add_row("[bold magenta]TYPE[/bold magenta]", stream.get("codec_type", "N/A"))
            sub_table.add_row(
                "[bold magenta]LANGUAGE[/bold magenta]",
                stream["tags"].get("language", "N/A") if "tags" in stream else "N/A",
            )

            if stream["codec_type"] == "video":
                sub_table.add_row(
                    "[bold magenta]RESOLUTION[/bold magenta]",
                    f"{stream.get('width', 'N/A')}x{stream.get('height', 'N/A')}",
                )
                sub_table.add_row(
                    "[bold magenta]DISPLAY ASPECT RATIO[/bold magenta]", stream.get("display_aspect_ratio", "N/A")
                )
                sub_table.add_row("[bold magenta]FRAME RATE[/bold magenta]", stream.get("r_frame_rate", "N/A"))
            elif stream["codec_type"] == "audio":
                sub_table.add_row("[bold magenta]CHANNELS[/bold magenta]", str(stream.get("channels", "N/A")))
                sub_table.add_row("[bold magenta]SAMPLE RATE[/bold magenta]", stream.get("sample_rate", "N/A"))

            self.console.print(sub_table)
