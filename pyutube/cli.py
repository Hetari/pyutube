# Command-line interface logic
import os
from .utils import (
    console,
    error_console,
    clear,
    is_internet_available,
    is_youtube_link,
    file_type,
    ask_resolution,
)
from .downloader import Downloader
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
    is_valid_link = is_youtube_link(url)

    if not is_valid_link[0]:
        console.print("❌ Invalid link", style="danger")
        return

    if is_valid_link[0] and is_valid_link[1].lower() == "video":
        # Determine the file type to download, is it audio or video?
        file = file_type().lower()

        if file.startswith("abort"):
            return

        elif file.startswith("cancel"):
            error_console.print("❗ Cancel the download...")
            return

        quality = ask_resolution()

        if quality.lower().startswith("cancel"):
            error_console.print("❗ Cancel the download...")
            return

        downloader = Downloader(
            url=url, path=path, quality=quality, is_audio=file.startswith(
                "audio"),
        )

    elif is_valid_link[0] and is_valid_link[1].lower() == "short":
        downloader = Downloader(
            url=url, path=path, quality="480p", is_short=True)

    downloader.download_video()

    del downloader
