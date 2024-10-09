"""
Pyutube is a command-line interface, a versatile tool
to download YouTube videos, shorts, and playlists.

This module provides a command-line interface (CLI), a powerful tool designed
to simplify the process of downloading YouTube content directly from the terminal.
Pyutube supports downloading videos (as video or audio), shorts, and playlists,
offering users flexibility and convenience in managing their media downloads.

Usage:
    $ pyutube download <URL> [options]

Options:
    -a, --audio          Download only audio.
    -f, --footage        Download only video (footage).
    -v, --version        Show the version number.

Example:
    $ pyutube <YouTube_URL> -a
        Download the audio of the specified YouTube video.

    $ pyutube <YouTube_URL> -f
        Download the video (footage) of the specified YouTube video.

    $ pyutube <YouTube_URL>
        Download the file of the specified YouTube video,
        it will ask you about downloading it as video or audio.

    $ pyutube <YouTube_playlist_URL>
        Download all videos from the specified YouTube playlist.

    $ pyutube <YouTube_short_URL>
        Download the specified YouTube short video.

Made with ❤️ By Ebraheem. Find me on GitHub: @Hetari. The project lives on @Hetari/pyutube.

Thank you for using Pyutube! Your support is greatly appreciated. ⭐️
"""

import os
import sys

import typer

from pyutube.utils import (
    __version__,
    __app__,
    clear,
    error_console,
    console,
    check_internet_connection,
    check_for_updates,
    play_notification
)
from pyutube.services import DownloadService
from pyutube.handlers import URLHandler

# Create CLI app
app = typer.Typer(
    name="pyutube",
    add_completion=False,
    help="Awesome CLI to download YouTube videos \
    (as video or audio)/shorts/playlists from the terminal",
    rich_markup_mode="rich",
)


# Define the variables for the arguments and options
url_arg = typer.Argument(
    None,
    help="YouTube URL [red]required[/red]",
    show_default=False
)
path_arg = typer.Argument(
    os.getcwd(),
    help="Path to save video [cyan]default: <current directory>[/cyan]",
    show_default=False
)
audio_option = typer.Option(
    False, "-a", "--audio", help="Download only audio"
)
video_option = typer.Option(
    False, "-f", "--footage", help="Download only video"
)
version_option = typer.Option(
    False, "-v", "--version", help="Show the version number"
)


@app.command(
    name="download",
    help="""
Download a [red]YouTube[/red] [green]videos[/green] [blue](as
video or audio)[/blue], [green]shorts[/green], and [green]playlists[/green].
    """,
    epilog="""
Made with ❤️  By Ebraheem. Find me on GitHub: [link=https://github.com/Hetari]@Hetari[/link].

The project lives on [link=https://github.com/Hetari/pyutube]@Hetari/pyutube[/link].\n\nThank you for using Pyutube! and your support :star:
""",
)
def pyutube(
    url: str = url_arg,
    path: str = path_arg,
    audio: bool = audio_option,
    video: bool = video_option,
    version: bool = version_option
) -> None:
    """
    Downloads a YouTube video.

    Args:
        url (str): The URL of the YouTube video.
        path (str): The path to save the video. Defaults to the current working directory.

    """
    if version:
        console.print(f"Pyutube {__version__}")
        check_for_updates()
        sys.exit()

    if url is None:
        error_console.print("❗ Missing argument 'URL'.")
        sys.exit()

    clear()

    if not check_internet_connection():
        sys.exit()

    url_handler = URLHandler(url)
    is_valid_link, link_type = url_handler.validate()

    if not is_valid_link:
        sys.exit()

    download_service = DownloadService(url, path, None)
    if audio:
        download_service.is_audio = True
        video, video_id,  _, video_audio, _ = download_service.download_preparing()
        download_service.download_audio(video, video_audio, video_id)

    elif video or link_type == "short":
        video, video_id,  streams, video_audio, quality = download_service.download_preparing()
        video_file = download_service.video_service.get_video_streams(quality, streams)
        download_service.download_video(video, video_id, video_file, video_audio)

    elif link_type == "video":
        download_service.asking_video_or_audio()

    elif link_type == "playlist":
        download_service = DownloadService(url, path, None)
        download_service.get_playlist_links()

    else:
        error_console.print("❗ Unsupported link type.")
        sys.exit()

    check_for_updates()
    play_notification()
    sys.exit()
