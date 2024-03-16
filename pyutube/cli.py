import os
import typer
from .utils import (
    clear,
    check_internet_connection,
    is_youtube_video_id,
    validate_link,
    handle_video_link,
)
from .downloader import download


# Create CLI app
app = typer.Typer(add_completion=False)


@app.command(name="download", help="Download a YouTube video")
def pyutube(
    url: str = typer.Argument(
        ...,
        help="YouTube URL",
        show_default=False),
    path: str = typer.Argument(
        os.getcwd(),
        help="Path to save video [default: <current directory>]",  show_default=False),
):
    """
    Downloads a YouTube video.

    Args:
        url (str): The URL of the YouTube video.
        path (str): The path to save the video. Defaults to the current working directory.

    Returns:
        None
    """
    clear()

    if not check_internet_connection():
        return

    if is_youtube_video_id(url):
        url = f"https://www.youtube.com/watch?v={url}"

    is_valid_link, link_type = validate_link(url)

    if not is_valid_link:
        return

    if link_type == "video":
        try:
            url, path, is_audio = handle_video_link(url, path)
        except TypeError:
            return

        download(url, path, is_audio)

    elif link_type == "short":
        download(url, path, is_audio)
