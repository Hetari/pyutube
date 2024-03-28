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
    help="Awesome CLI to download YouTube videos(as video or audio)/shorts/playlists from the terminal",
    rich_markup_mode="rich",
)


@app.command(
    name="download",
    help="Download a [red]YouTube[/red] [green]videos[/green] [blue](as video or audio)[/blue], [green]shorts[/green], and [green]playlists[/green].",
    epilog=f"Made with ❤️  By Ebraheem. Find me on GitHub: [link=https://github.com/Hetari]@Hetari[/link]. The project lives on [link=https://github.com/Hetari/pyutube]@Hetari/pyutube[/link].\n\nThank you for using Pyutube! and your support :star:\n",
)
def pyutube(
    url: str = typer.Argument(
        None,
        help="YouTube URL [red]required[/red]",
        show_default=False),
    path: str = typer.Argument(
        os.getcwd(),
        help="Path to save video [cyan]default: <current directory>[/cyan]",  show_default=False),
    audio: bool = typer.Option(
        False, "-a", "--audio", help="Download only audio"
    ),
    video: bool = typer.Option(
        False, "-f", "--footage", help="Download only video"
    ),
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

    elif audio:
        download(url, path, is_audio=True)

    elif video or link_type == "short":
        download(url, path, is_audio=False)

    elif link_type == "video":
        # ask if the user wants to download audio, or video?
        try:
            is_audio = handle_video_link(url, path)
        except TypeError:
            return
        download(url, path, is_audio)

    elif link_type == "playlist":
        try:
            is_audio = handle_video_link(url, path)
        except TypeError:
            return
        playlist = download(url, path, is_audio, is_playlist=True)
        links = playlist.video_urls
        title = playlist.title

        if not links:
            error_console.print("❗ There are no videos in the playlist.")
            return

        console.print(f"\nPlaylist title: {title}", style="info")
        console.print(f"Total videos: {len(links)}\n", style="info")
        console.print("")

        for index, link in enumerate(links):
            if index == 0:
                quality = download(links[0], path, is_audio)
            download(link, path, is_audio, quality_choice=quality)
            clear()

    else:
        error_console.print("❗ Unsupported link type.")
        return False

    return True
