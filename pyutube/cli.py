# Command-line interface logic
import os
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


# Create CLI app
app = typer.Typer()


@app.command(name="download", help="Download a YouTube video")
def download(
    url: str = typer.Argument(..., help="YouTube video URL"),
    path: str = typer.Argument(os.getcwd(), help="Path to save video"),
):
    """
    Downloads a YouTube video.

    Args:
        url: The URL of the YouTube video.
        path: The path to save the video. Defaults to the current working directory.

    Returns:
        None
    """
    # Clear the console
    clear()

    # Check if internet is available
    if not is_internet_available():
        error_console.print("❗ No internet connection")
        return

    console.print("✅ There is internet connection", style="info")
    console.print()

    # Check if the link is valid youtube link
    if is_valid_link := not is_youtube_link(url):
        console.print("❌ Invalid link", style="danger")
        return

    # Determine the file type to download, is it audio or video?
    file = file_type().lower()

    # Choose download option based on file type
    match file:
        case "audio":
            download_video(url=url, path=path, is_audio=True,)
        case "video":
            quality = ask_resolution()
            download_video(url=url, quality=quality, path=path)
        case "cancel the download":
            return
