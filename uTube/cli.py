# Command-line interface logic
from .utils import (
    __app_name__,
    __version__,
    console,
    welcome,
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


@app.command(name="info", help="Get information about the app")
def info():
    console.print(f"{__app_name__} v {__version__}", style="info")


@app.command(name="download", help="Download a YouTube video")
def download(url: str = typer.Argument(...)):
    clear()
    if is_internet_available():
        console.print("✅ There is internet connection", style="info")
        console.print()

        if is_valid_link := is_youtube_link(url):
            file = file_type()
            if file["file_type"] == "audio":
                # download_vide(url, "audio")
                ...
            else:
                quality = ask_resolution()
                download_video(url, quality)
        else:
            console.print("❌ Invalid link", style="danger")
    else:
        console.print("❗ No internet connection", style="danger")
