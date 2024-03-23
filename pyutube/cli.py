import os

import typer

from .utils import (
    __version__,
    clear,
    error_console,
    console,
    check_internet_connection,
    is_youtube_video_id,
    validate_link,
    handle_video_link,
)
from .downloader import download


# Create CLI app
app = typer.Typer(
    name="pyutube",
    add_completion=False,
    help="Awesome CLI to download YouTube videos(as video or audio)/shorts from the terminal",
    rich_markup_mode="rich",
)


@app.command(
    name="download",
    help="Download a [red]YouTube[/red] videos (as video or audio), shorts, (playlists soon as possible).",
    epilog="Made with ❤️  By Ebraheem. Find me on GitHub: [link=https://github.com/Hetari]click here @Hetari[/link]",
)
def pyutube(
    url: str = typer.Argument(
        None,
        help="YouTube URL [red]required[/red]",
        show_default=False),
    path: str = typer.Argument(
        os.getcwd(),
        help="Path to save video [cyan]default: <current directory>[/cyan]",  show_default=False),
    version: bool = typer.Option(
        False, "-v", "--version", help="Show the version number"),
):
    """
    Downloads a YouTube video.

    Args:
        url (str): The URL of the YouTube video.
        path (str): The path to save the video. Defaults to the current working directory.

    """
    if version:
        console.print(f"Pyutube {__version__}")
        return

    if url is None:
        error_console.print("❗ Missing argument 'URL'.")
        return

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
        console.print("✅ Download completed", style="info")

    elif link_type == "short":
        download(url, path, is_audio=False)
        console.print("✅ Download completed", style="info")

    else:
        error_console.print("❗ Unsupported link type.")
        return False

    return True
