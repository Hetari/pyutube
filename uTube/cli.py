# Command-line interface logic
from .utils import (
    __app_name__,
    __version__,
    console,
    error_console,
    clear,
    is_internet_available,
    is_youtube_link,
    file_type,
    ask_resolution,
)

from .downloader import download_video

import typer
import rich


app = typer.Typer()


@app.command(name="download", help="Download a YouTube video")
def download(url: str = typer.Argument(...)):
    clear()
    if is_internet_available():
        console.print("✅ There is internet connection", style="info")
        console.print()

        if is_valid_link := is_youtube_link(url):
            file = file_type()
            if file == "audio":
                download_video(url, is_audio=True)
            else:
                quality = ask_resolution()
                download_video(url, quality)
        else:
            console.print("❌ Invalid link", style="danger")
    else:
        error_console.print("❗ No internet connection")
