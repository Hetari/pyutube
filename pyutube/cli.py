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
import re

import typer
import threading

from pyutube.utils import (
    __version__,
    __app__,
    clear,
    error_console,
    console,
    check_internet_connection,
    is_youtube_video_id,
    validate_link,
    handle_video_link,
    ask_playlist_video_names,
    check_for_updates
)
from pyutube.downloader import download


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

    if is_youtube_video_id(url):
        url = f"https://www.youtube.com/watch?v={url}"

    is_valid_link, link_type = validate_link(url)

    if not is_valid_link:
        sys.exit()

    if audio:
        download(url, path, is_audio=True)

    elif video or link_type == "short":
        download(url, path, is_audio=False)

    elif link_type == "video":
        handle_video(url, path)

    elif link_type == "playlist":
        handle_playlist(url, path)

    else:
        error_console.print("❗ Unsupported link type.")
        sys.exit()

    check_for_updates()
    sys.exit()


def handle_video(url, path):
    """
    Downloads a video from the given URL and saves it to the specified path.

    Args:
        url (str): The URL of the video.
        path (str): The path to save the video.

    Returns:
        None
    """
    # ask if the user wants to download audio, or video?
    try:
        is_audio = handle_video_link()
    except TypeError:
        return
    download(url, path, is_audio)


def handle_playlist(url: str, path: str):
    """
    Downloads a playlist of videos from the given URL and saves them to the specified path.

    Args:
        url (str): The URL of the playlist.
        path (str): The path to save the downloaded videos.

    Returns:
        None
    """

    def fetch_title_thread(video):
        """Fetch the title of a YouTube video in a separate thread."""
        video_title = safe_filename(video.title)
        video_id = video.video_id
        playlist_videos.append((video_title, video_id))

    global playlist_videos

    try:
        is_audio = handle_video_link()
    except TypeError:
        return
    playlist = download(url, path, is_audio, is_playlist=True)

    # links = playlist.video_urls
    title = playlist.title
    total = playlist.length
    videos = playlist.videos

    # Use threading to fetch titles concurrently
    title_threads = []
    playlist_videos = []  # List to store video titles

    # Create and start a thread for each video
    for video in videos:
        thread = threading.Thread(target=fetch_title_thread, args=(video,))
        thread.start()
        title_threads.append(thread)

    # Wait for all threads to finish
    for thread in title_threads:
        thread.join()

    # Now all video titles are stored in the video_titles list
    console.print(f"\nPlaylist title: {title}\n", style="info")
    console.print(f"Total videos: {total}\n", style="info")

    os.makedirs(title, exist_ok=True)
    new_path = os.path.join(path, title)

    # check if there is any video already downloaded in the past
    for file in os.listdir(new_path):
        for video in playlist_videos:
            if file.startswith(video):
                playlist_videos.remove(video)
                # Exit the inner loop since we found a match
                break

    if not playlist_videos:
        console.print(f"All playlist are already downloaded in this directory, see '{
                      title}' folder", style="info")
        sys.exit()

    console.print("Chose what video you want to download")
    videos_selected = ask_playlist_video_names(playlist_videos)

    for index, video_id in enumerate(videos_selected):
        url = f"https://www.youtube.com/watch?v={video_id}"

        if index == 0:
            quality = download(url, new_path, is_audio, is_playlist=False)
            continue
        download(url, new_path, is_audio,
                 quality_choice=quality,
                 is_playlist=False)


def safe_filename(s: str, max_length: int = 255) -> str:
    """Sanitize a string making it safe to use as a filename.

    This function was based off the limitations outlined here:
    https://en.wikipedia.org/wiki/Filename.

    :param str s:
        A string to make safe for use as a file name.
    :param int max_length:
        The maximum filename character length.
    :rtype: str
    :returns:
        A sanitized string.
    """
    # Characters in range 0-31 (0x00-0x1F) are not allowed in ntfs filenames.
    ntfs_characters = [chr(i) for i in range(31)]
    characters = [
        r'"',
        r"\#",
        r"\$",
        r"\%",
        r"'",
        r"\*",
        r"\,",
        r"\.",
        r"\/",
        r"\:",
        r'"',
        r"\;",
        r"\<",
        r"\>",
        r"\?",
        r"\\",
        r"\^",
        r"\|",
        r"\~",
        r"\\\\",
    ]
    pattern = "|".join(ntfs_characters + characters)
    regex = re.compile(pattern, re.UNICODE)
    filename = regex.sub("", s)
    return filename[:max_length].rsplit(" ", 0)[0]
