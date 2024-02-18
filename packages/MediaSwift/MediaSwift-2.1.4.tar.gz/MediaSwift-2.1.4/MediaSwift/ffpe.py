# ffpe.py
# -------------

import os
import gc
import subprocess
from threading import Thread
import logging
from typing import Optional, List
from functools import lru_cache
from rich.console import Console


def clear_console():
    # CLEAR CONSOLE SCREEN
    """
    >>> CLEAR SCREEN FUNCTION
    """
    if os.name == "nt":
        _ = os.system("cls")  # FOR WINDOWS
    else:
        _ = os.system("clear")  # FOR LINUX/MACOS


class ffpe:
    """
    >>> FFPE - SIMPLE WRAPPER FOR FFMPEG.

    >>> THIS CLASS PROVIDES CONVENIENT INTERFACE FOR USING FFMPEG TO CONVERT MULTIMEDIA FILES.

    ATTRIBUTES:
    ----------
    >>> -FFpe_PATH : STR
        >>> PATH TO THE FFMPEG EXECUTABLE.
    >>> -LOGGER : LOGGING.LOGGER
        >>> LOGGER INSTANCE FOR LOGGING MESSAGES.

    METHODS:
    ----------
    >>> CONVERT(INPUT_FILES, OUTPUT_DIR, CV=NONE, CA=NONE, S=NONE, HWACCEL=NONE,
    >>>         AR=NONE, AC=NONE, BA=NONE, R=NONE, F=NONE, PRESET=NONE, BV=NONE)
    >>>     CONVERT MULTIMEDIA FILES USING FFMPEG.

    CONVERT( )
    ----------
        >>> NOTE: USE "convert()" TO CONVERT MEDIA FILES.

        >>> EXAMPLE


        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         # INSTANTIATE THE FFPE CLASS

         from MediaSwift import *
         ffpe_instance = ffpe()

         # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        ... input_files = [r'input1.mp4', r'input2.mp4'] # input_files [MULTIPLE CONVERT]
        ... input_file = [r'input1.mp4']                 # input_file [SINGLE CONVERT]

         output_dir = r'output_folder'

         # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG.
         ffpe_instance.convert(
             input_files=input_files,
             output_dir=output_dir,
             cv='h264',        # VIDEO CODEC
             ca='aac',         # AUDIO CODEC
             s='1920x1080',    # VIDEO RESOLUTION
             hwaccel='cuda',   # HARDWARE ACCELERATION
             ar=44100,         # AUDIO SAMPLE RATE
             ac=2,             # AUDIO CHANNELS
             ba='192k',        # AUDIO BITRATE
             r=30,             # VIDEO FRAME RATE
             f='mp4',          # OUTPUT FORMAT
             preset='fast',    # PRESET FOR ENCODING
             bv=2000           # VIDEO BITRATE
         )
        NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS:
        EXAMPLE_1 - input_files=[r"PATH_TO_INPUT_FILE"] # SINGLE CONVERTION
        EXAMPLE_2 - input_files=[
                                r"PATH_TO_INPUT_FILE_1",
                                r"PATH_TO_INPUT_FILE_2"] # MULTIPLE CONVERTION
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
    CODECS( )
    ----------
        >>> GET INFORMATION ABOUT AVAILABLE CODECS USING FFMPEG.

    FORMATS( )
    ---------
       >>> GET INFORMATION ABOUT AVAILABLE FORMATS USING FFMPEG.

    >>> RETURNS: NONE

    """

    def __init__(self):
        """
        >>> INITIALIZE THE FFPE INSTANCE.

        >>> SETS THE DEFAULT PATH TO THE FFMPEG EXECUTABLE AND INITIALIZES THE LOGGER.
        """
        self.ffpe_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffpe.exe"
        )
        self.logger = self._initialize_logger()

    def _initialize_logger(self) -> logging.Logger:
        """
        >>> INITIALIZE THE LOGGER FOR LOGGING MESSAGES.

        RETURNS
        -------
        >>> LOGGING.LOGGER
            >>> LOGGER INSTANCE.
        """
        logger = logging.getLogger("ffpe_logger")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

    def convert(
        self,
        input_files: Optional[List[str]] = None,
        input_file: Optional[str] = None,
        output_dir: Optional[str] = None,
        cv: Optional[str] = None,
        ca: Optional[str] = None,
        s: Optional[str] = None,
        hwaccel: Optional[str] = None,
        ar: Optional[int] = None,
        ac: Optional[int] = None,
        ba: Optional[int] = None,
        r: Optional[int] = None,
        f: Optional[str] = None,
        preset: Optional[str] = None,
        bv: Optional[int] = None,
    ) -> None:
        """
            >>> EXAMPLE

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         # INSTANTIATE THE FFPE CLASS

         from MediaSwift import *
         ffpe_instance = ffpe()

         # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        ... input_files = [r'input1.mp4', r'input2.mp4'] # input_files [MULTIPLE CONVERT]
        ... input_file = [r'input1.mp4']                 # input_file [SINGLE CONVERT]

         output_dir = r'output_folder'

         # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG.
         ffpe_instance.convert(
             input_files=input_files,
             output_dir=output_dir,
             cv='h264',        # VIDEO CODEC
             ca='aac',         # AUDIO CODEC
             s='1920x1080',    # VIDEO RESOLUTION
             hwaccel='cuda',   # HARDWARE ACCELERATION
             ar=44100,         # AUDIO SAMPLE RATE
             ac=2,             # AUDIO CHANNELS
             ba='192k',        # AUDIO BITRATE
             r=30,             # VIDEO FRAME RATE
             f='mp4',          # OUTPUT FORMAT
             preset='fast',    # PRESET FOR ENCODING
             bv=2000           # VIDEO BITRATE
         )
        NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS:
        EXAMPLE_1 - input_files=[r"PATH_TO_INPUT_FILE"] # SINGLE CONVERTION
        EXAMPLE_2 - input_files=[
                                r"PATH_TO_INPUT_FILE_1",
                                r"PATH_TO_INPUT_FILE_2"] # MULTIPLE CONVERTION

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        ADDITIONAL NOTE:
        ----------------
        >>> USE "input_files" FOR MULTIPLE FILE CONVERSION, USE "input_file" SINGLE CONVERSION.
        >>> REMEMBER ALWAYS USE SQUARE BRACKETS FOR INPUT FILE PATH.
        >>> RETURNS: NONE

        """

        if not input_files and not input_file:
            self.logger.error("No input files provided.")
            return

        # HANDLE SINGLE FILE CONVERSION WITHOUT SQUARE BRACKETS
        if input_file:
            input_files = [input_file]

        threads = []
        for input_file in input_files:
            # EXTRACT THE FILENAME FROM THE INPUT PATH
            filename = os.path.basename(input_file)

            # CREATE THE OUTPUT FILE PATH BY JOINING THE OUTPUT_DIR AND FILENAME
            output_file = os.path.join(output_dir, filename)

            # CREATE A THREAD FOR EACH CONVERSION
            t = Thread(
                target=self._convert_single,
                args=(
                    input_file,
                    output_file,
                    cv,
                    ca,
                    s,
                    hwaccel,
                    ar,
                    ac,
                    ba,
                    r,
                    f,
                    preset,
                    bv,
                ),
            )
            threads.append(t)
            t.start()

        # WAIT FOR ALL THREADS TO FINISH
        for thread in threads:
            thread.join()

    @lru_cache(maxsize=None)
    def _convert_single(
        self,
        input_file: str,
        output_file: str,
        cv: Optional[str] = None,
        ca: Optional[str] = None,
        s: Optional[str] = None,
        hwaccel: Optional[str] = None,
        ar: Optional[int] = None,
        ac: Optional[int] = None,
        ba: Optional[int] = None,
        r: Optional[int] = None,
        f: Optional[str] = None,
        preset: Optional[str] = None,
        bv: Optional[int] = None,
    ) -> None:
        """

            >>> EXAMPLE

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         # INSTANTIATE THE FFPE CLASS

         from MediaSwift import *
         ffpe_instance = ffpe()

         # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        ... input_files = [r'input1.mp4', r'input2.mp4'] # input_files [MULTIPLE CONVERT]
        ... input_file = [r'input1.mp4']                 # input_file [SINGLE CONVERT]

         output_dir = r'output_folder'

         # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG.
         ffpe_instance.convert(
             input_files=input_files,
             output_dir=output_dir,
             cv='h264',        # VIDEO CODEC
             ca='aac',         # AUDIO CODEC
             s='1920x1080',    # VIDEO RESOLUTION
             hwaccel='cuda',   # HARDWARE ACCELERATION
             ar=44100,         # AUDIO SAMPLE RATE
             ac=2,             # AUDIO CHANNELS
             ba='192k',        # AUDIO BITRATE
             r=30,             # VIDEO FRAME RATE
             f='mp4',          # OUTPUT FORMAT
             preset='fast',    # PRESET FOR ENCODING
             bv=2000           # VIDEO BITRATE
         )
        NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS:
        EXAMPLE_1 - input_files=[r"PATH_TO_INPUT_FILE"] # SINGLE CONVERTION
        EXAMPLE_2 - input_files=[
                                r"PATH_TO_INPUT_FILE_1",
                                r"PATH_TO_INPUT_FILE_2"] # MULTIPLE CONVERTION

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        ADDITIONAL NOTE:
        ----------------
        >>> USE "input_files" FOR MULTIPLE FILE CONVERSION, USE "input_file" SINGLE CONVERSION.
        >>> REMEMBER ALWAYS USE SQUARE BRACKETS FOR INPUT FILE PATH.
        >>> RETURNS: NONE

        """
        # BUILD THE FFMPEG COMMAND BASED ON THE PROVIDED PARAMETERS
        command = [self.ffpe_path, "-hide_banner"]

        if hwaccel:
            command += ["-hwaccel", hwaccel]

        command += ["-i", input_file]

        if cv:
            command += ["-c:v", cv]
        if ca:
            command += ["-c:a", ca]
        if s:
            command += ["-s", s]
        if ar:
            command += ["-ar", str(ar)]
        if ac:
            command += ["-ac", str(ac)]
        if ba:
            command += ["-b:a", str(ba)]
        if r:
            command += ["-r", str(r)]
        if f:
            command += ["-f", f]
        if preset:
            command += ["-preset", preset]
        if bv:
            command += ["-b:v", str(bv)]

        if output_file:
            command += ["-y", output_file]

        try:
            # EXECUTE THE FFMPEG COMMAND
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            clear_console()
            print(f"FFPE COMMAND FAILED WITH ERROR: {e}")
        except Exception as e:
            clear_console()
            print(f"AN ERROR OCCURRED: {e}")

        # CALL THE GARBAGE COLLECTOR TO FREE UP RESOURCES
        gc.collect()

    @lru_cache(maxsize=None)
    def codecs(self) -> None:
        """
            >>> GET INFORMATION ABOUT AVAILABLE CODECS USING FFPE.

        >>> EXAMPLE


        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            >>> from MediaSwift import *
            >>> info = ffpe()
            >>> info.codecs()
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```

        >>> RETURNS: NONE
        """
        command = [self.ffpe_path, "-codecs"]
        console = Console()

        try:
            # Import the Table class
            from rich.table import Table

            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            output = result.stdout.decode("utf-8")
            lines = output.split("\n")

            # Use Rich Table for formatting
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("CODECS", style="cyan", width=20)
            table.add_column("TYPE", style="green", width=25)
            table.add_column("DESCRIPTION", style="yellow", width=100)
            table.add_column("FEATURES", style="cyan", width=20)

            for line in lines[11:]:  # Skip the header lines
                if line:  # Skip empty lines
                    fields = line.split()
                    if len(fields) >= 4:  # Ensure there are enough fields
                        codec_name = fields[1]
                        codec_type = fields[2].strip("()")
                        codec_description = " ".join(fields[3:])
                        features = fields[0]

                        # Extracting additional features
                        features_str = (
                            (".D" if "D" in features else "")
                            + (".E" if "E" in features else "")
                            + (".V" if "V" in features else "")
                            + (".A" if "A" in features else "")
                            + (".S" if "S" in features else "")
                            + (".T" if "T" in features else "")
                            + (".I" if "I" in features else "")
                            + (".L" if "L" in features else "")
                        )

                        table.add_row(
                            codec_name, codec_type, codec_description, features_str
                        )

            # PRINT THE LEGEND WITH COLORS
            legend = "\n".join(
                [
                    "[bold magenta]CODECS FEATURES LEGEND:[/bold magenta]",
                    "[cyan] D.....[/cyan] = DECODING SUPPORTED",
                    "[cyan] .E....[/cyan] = ENCODING SUPPORTED",
                    "[green] ..V...[/green] = VIDEO CODEC",
                    "[green] ..A...[/green] = AUDIO CODEC",
                    "[green] ..S...[/green] = SUBTITLE CODEC",
                    "[cyan] ..D...[/cyan] = DATA CODEC",
                    "[cyan] ..T...[/cyan] = ATTACHMENT CODEC",
                    "[cyan] ...I..[/cyan] = INTRA FRAME-ONLY CODEC",
                    "[cyan] ....L.[/cyan] = LOSSY COMPRESSION",
                    "[cyan] .....S[/cyan] = LOSSLESS COMPRESSION",
                ]
            )
            console.print(legend)
            console.print("━━━━━━━━━━━━━━━━━━━━━━")
            console.print(table)
        except subprocess.CalledProcessError as e:
            clear_console()
            console.print(f"[bold red]FFPE COMMAND FAILED WITH ERROR: {e}[/bold red]")
        except Exception as e:
            clear_console()
            console.print(f"[bold red]AN ERROR OCCURRED: {e}[/bold red]")

        gc.collect()

    @lru_cache(maxsize=None)
    def formats(self) -> None:  # CALL THE GARBAGE COLLECTOR TO FREE UP RESOURCES
        """
            >>> GET INFORMATION ABOUT AVAILABLE FORMATS USING FFMPEG.

        >>> EXAMPLE

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            >>> from MediaSwift import *
            >>> info = ffpe()
            >>> info.formats()
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```

        >>> RETURNS: NONE
        """
        command = [self.ffpe_path, "-formats"]
        console = Console()

        try:
            # IMPORT THE TABLE CLASS
            from rich.table import Table

            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            output = result.stdout.decode("utf-8")
            lines = output.split("\n")

            # USE RICH TABLE FOR FORMATTING
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("FORMAT", style="cyan", width=30)
            table.add_column("DESCRIPTION", style="yellow", width=50)
            table.add_column("FEATURES", style="cyan", width=50)

            for line in lines[5:]:  # SKIP THE HEADER LINES
                if line:  # SKIP EMPTY LINES
                    fields = line.split()
                    if len(fields) >= 2:  # ENSURE THERE ARE ENOUGH FIELDS
                        format_name = fields[1]
                        format_description = " ".join(fields[2:])
                        features = fields[0]

                        # EXTRACTING ADDITIONAL FEATURES
                        features_str = (
                            (".D" if "D" in features else "")
                            + (".E" if "E" in features else "")
                            + (".V" if "V" in features else "")
                            + (".A" if "A" in features else "")
                            + (".S" if "S" in features else "")
                            + (".T" if "T" in features else "")
                            + (".I" if "I" in features else "")
                            + (".L" if "L" in features else "")
                        )

                        table.add_row(format_name, format_description, features_str)

            legend = "\n".join(
                [
                    "[bold magenta]FILE FORMATS FEATURES LEGEND:[/bold magenta]",
                    "[green] D.[/green] = DEMUXING SUPPORTED",
                    "[cyan] .E[/cyan] = MUXING SUPPORTED",
                ]
            )
            console.print(legend)
            console.print("━━━━━━━━━━━━━━━━━━━━━━")
            console.print(table)
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]FFPE COMMAND FAILED WITH ERROR: {e}[/bold red]")
        except Exception as e:
            console.print(f"[bold red]AN ERROR OCCURRED: {e}[/bold red]")

        gc.collect()


# CALL THE GARBAGE COLLECTOR TO FREE UP RESOURCES
