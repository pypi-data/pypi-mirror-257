## `MediaSwift` - EMPOWERING PYTHON WITH ADVANCED MULTIMEDIA OPERATIONS.

[![License](https://img.shields.io/badge/LICENSE-GPLv3-blue.svg)](https://github.com/yourusername/MediaSwift/blob/main/LICENSE)

#### A POWERFUL PYTHON LIBRARY FOR SEAMLESS MULTIMEDIA OPERATIONS. `MediaSwift` SIMPLIFIES COMPLEX TASKS, MAKING IT EASY TO INTEGRATE AND ENHANCE YOUR MULTIMEDIA APPLICATIONS. DIVE INTO THE FUTURE OF MEDIA HANDLING WITH `MediaSwift` - YOUR GO-TO LIBRARY FOR 2024.

**KEY FEATURES:**
- **EFFORTLESS FILE CONVERSION .**
- **SEAMLESS MULTIMEDIA PLAYBACK .**
- **PROVIDING INFORMATION `MediaSwift` ALSO OFFERS DETAILED MULTIMEDIA INFORMATION RETRIEVAL .**


### EXPLORE THE CAPABILITIES OF `MediaSwift` AND ELEVATE YOUR PYTHON MULTIMEDIA PROJECTS WITH SIMPLICITY AND EFFICIENCY.


### SUPPORTED VIDEO CODECS
`h264`, `libx264`, `mpeg4`, `vp9`, `av1`, `hevc`, `mjpeg`, `H.265 / HEVC`, `VP8`, `VP9`, `AV1`, `VC1`, `MPEG1`, `MPEG2`, `H.263`, `Theora`, `MJPEG`, `MPEG-3`, `MPEG-4`, AND MORE.

### SUPPORTED AUDIO CODECS
`aac`, `mp3`, `opus`, `vorbis`, `pcm`, `alac`, `flac`, `wv`, `ape`, `mka`, `opus`, `ac3`, `eac3`, `alac`, AND MORE.

### SUPPORTED FILE EXTENSIONS
**VIDEO FORMATS:** `.mp4`, `.avi`, `.mkv`, `.webm`, `.mov`, `.wmv`, `.webm`, `.flv`, `.mov`, `.wmv`, `.hevc`, `.prores`, `.dv`
**AUDIO FORMATS:** `.mp3`, `.aac`, `.ogg`, `.wav`, `.flac`, `.flac`, `.m4a`, `.ogg`, `.wv`, `.ape`, `.mka`, `.opus`, `mpc`, `.tak`, `.alac`, AND MORE .


**NOTE: ALSO SUPPORT DOLBY DIGITAL PLUS AND DOLBY DIGITALAUDIO CODEC `.eac3`, `.ac3`
AND SUPPORT MORE VIDEO AND AUDIO CODECS AND VARIOUS [FORMATE EXTENSION].**

**`MediaSwift`: A VERSATILE LIBRARY WITH MANY SUPPORT AUDIO AND VIDEO CODECS, AS WELL AS MULTIPLE FILE FORMATS EXTENSION.**


## LIST THE AVAILABLE CODECS AND FORMATES:
```python
from MediaSwift import ffpe

ffpe_instance = ffpe()

ffpe_instance.formats()
ffpe_instance.codecs()
```

#### USE `.formate()` AND `.codecs()` METHOD.

## CHECK LIBRARY VERSION USING:

```python
from MediaSwift import version

version_info = version()
print(version_info)
```

## PLAY MEDIA USING ffpl
#### THE `ffpl` CLASS PROVIDES METHODS FOR PLAY MEDIA FILES. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHODS:

```python
from MediaSwift import ffpl

play = ffpl()
media_file = r"PATH_TO_INPUT_FILE"
play.play(media_file)
```

#### USE THE `.play()` METHOD TO PLAY MEDIA.

## USING THE `ffpr` CLASS

#### THE `ffpr` CLASS PROVIDES METHODS FOR PROBING MEDIA FILES. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHODS:

```python
from MediaSwift import ffpr

ffpr_info = ffpr()

info = ffpr_info.probe(r"PATH_TO_INPUT_FILE")
ffpr_info.pretty(info)
```

#### IN THIS EXAMPLE, REPLACE `"PATH_TO_MEDIA_FILE"` WITH THE ACTUAL PATH TO YOUR MEDIA FILE. THE `.probe` METHOD RETURNS A DICTIONARY CONTAINING INFORMATION ABOUT THE MEDIA FILE. THE `.pretty`

## USING THE `ffpe` CLASS

#### THE `ffpe` CLASS PROVIDES METHODS FOR VIDEO CONVERSION, LISTING CODECS, AND LISTING FORMATS. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHODS:

#### - EXAMPLE - CONVERT SINGLE VIDEO USING THIS: 
```python
from MediaSwift import ffpe

ffmpe = ffpe()

ffmpe.convert(
    input_file=[r"PATH_TO_INPUT_FILE"],
    output_dir=r"PATH_TO_OUTPUT_FILE",
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
    bv='2000k'        # VIDEO BITRATE 
)
```
#### - EXAMPEL - CONVERT MULTIPLE VIDEO USING THIS: 
**- NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS:**
```python
from MediaSwift import ffpe

ffpe_instance = ffpe()

input_files = [
    r"PATH_TO_INPUT_FILE",
    r"PATH_TO_INPUT_FILE",
    # ADD MORE FILE PATHS AS NEEDED
]
output_directory = r"PATH_TO_OUTPUT_FILE"

ffpe_instance.convert_with_threading(
    file_list=input_files,
    output_dir=output_directory,
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
    bv='2000k'        # VIDEO BITRATE
)
```
#### USE THE `.convert()` METHOD TO CONVERT MEDIA.
**- NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS:**


## IMPORT CLASS:
```python
from MediaSwift import ffpe, ffpl, ffpr
from MediaSwift import *
```

## INSTALLATION:

```bash
pip install MediaSwift
```
##  CONTACT

**THIS PROJECT IS MAINTAINED BY [ROHIT SINGH]. FOR ANY QUERIES OR CONTRIBUTIONS TO CHECK MY GITHUB, PLEASE REACH OUT TO US. THANK YOU FOR USING `MediaSwift` PYTHON LIBRARY, NEW LIBRARY RELEASE 2024 .**

