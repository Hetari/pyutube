# Command-line interface logic
from .utils import (
    __app_name__,
    __version__,
    console,
    welcome,
    clear,
    is_internet_available,
)

from .downloader import download_vide

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

        download_vide(url)
    else:
        console.print("❗ No internet connection", style="danger")
