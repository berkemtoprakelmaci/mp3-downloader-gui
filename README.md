# MP3 Downloader GUI

This project is a graphical interface built using Python and PySide6 for downloading audio from supported media URLs using yt-dlp.

## Disclaimer

This software is provided for educational purposes only.

Users are responsible for complying with the terms of service of the websites they use.

Do not use this software to download copyrighted material without permission.

The author is not responsible for any misuse of this software.

## Requirements

- Python 3.10+
- FFmpeg installed and added to PATH

Download FFmpeg from:
https://ffmpeg.org/download.html

## Installation
Copy the ffmpeg.exe and ffprobe.exe files next to .py file. 
For .py to .exe (cmd should be opened in the directory that consist .py file):
`pip3 install pyinstaller` (if pyinstaller is installed already not needed)
`pyinstaller --noconsole --onefile --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." mp3_downloader.py`
