"""
This module contains the utils functions for the pyutube package.
"""

import sys
import re
import os
from datetime import timedelta

import inquirer
import requests
from yaspin import yaspin
from yaspin.spinners import Spinners
from rich.console import Console
from rich.theme import Theme
from termcolor import colored


__version__ = "1.2.9"
__app__ = "pyutube"
ABORTED_PREFIX = "aborted"
CANCEL_PREFIX = "Cancel"


# Set up the console
custom_theme = Theme({
    "info": "#64b0f2",
    "warning": "color(3)",
    "danger": "red",
    "success": "green",
})
console = Console(theme=custom_theme)
error_console = Console(stderr=True, style="red")


def clear() -> None:
    """
    Function to clear the console screen, it can be used for any operating system

    Args:
        This function does not take any parameters.

    Returns:
        It does not return anything (None).
    """
    # For Windows
    if os.name == "nt":
        os.system("cls")
    else:
        # For Unix/Linux/MacOS
        os.system("clear")


@yaspin(text="Checking internet connection", color="blue", spinner=Spinners.earth)
def is_internet_available() -> bool:
    """
    Checks if internet connection is available by making a simple request
    to http://www.google.com with a timeout of 5 seconds.

    Returns:
        bool: the request status (True if available, False if not).
    """
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except Exception:
        return False


def is_youtube_link(link: str) -> tuple[bool, str]:
    """
    Check if the given link is a YouTube video, playlist, or shorts link.

    Args:
        link (str): The link to be checked.

    Returns:
        tuple[bool, str]: True if the link is a YouTube video, playlist, or shorts link,
        False otherwise. The second item of the tuple indicates the type of link found:
        'video', 'playlist', or 'shorts'.
    """
    is_video = is_youtube_video(link)
    is_short = is_youtube_shorts(link)
    is_playlist = is_youtube_playlist(link)

    return (is_video, "video") if is_video \
        else (is_short, "short") if is_short \
        else (True, "playlist") if is_playlist\
        else (False, "unknown")


def is_youtube_shorts(link: str) -> bool:
    """
    Check if the given link is a YouTube shorts link.

    Args:
        link: The link to be checked.

    Returns:
        bool: True if the link is a YouTube shorts link, False otherwise.
    """
    # shorts_pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]+)"
    shorts_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|shorts\/|watch\?.*?v=))(?:(?:[^\/\n\s]+\/)?)([a-zA-Z0-9_-]+)"
    shorts_match = re.match(shorts_pattern, link)
    return bool(shorts_match)


def is_youtube_video(link: str) -> bool:
    """
    Check if the given link is a YouTube video.

    Args:
        link: The link to be checked.

    Returns:
        bool: True if the link is a YouTube video, False otherwise.
    """
    # video_pattern = re.compile(
    # r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:(?:live/?[a-zA-Z0-9_-]{11}\?si=)|(?:(?:watch\?v=)|(?:embed/))|youtu\.be/|youtube.com/share\?v=)([a-zA-Z0-9_-]{11}))')
    # video_pattern = re.compile(
    # r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:(?:watch\?v=)|(?:embed/))|youtu\.be/|youtube.com/share\?v=)([a-zA-Z0-9_-]{11})')
    video_pattern = re.compile(
        # "https://www.youtube.com/watch?time_continue=1&v=dQw4w9WgXcQ"
        r"^(?:https?://)?(?:www\.)?(?:youtube(?:-nocookie)?\.com/(?:(watch\?v=|watch\?feature\=share\&v=)|embed/|v/|live_stream\?channel=|live\/)|youtu\.be/)([a-zA-Z0-9_-]{11})"
    )

    return bool(video_pattern.match(link))


def is_youtube_playlist(link: str) -> bool:
    """
    Check if the given link is a YouTube playlist.

    Args:
        link: The link to be checked.

    Returns:
        bool: True if the link is a YouTube playlist, False otherwise.
    """
    playlist_pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/playlist\?list=([a-zA-Z0-9_-]+)"
    playlist_match = re.match(playlist_pattern, link)
    return bool(playlist_match)


def is_youtube_video_id(video_id: str) -> bool:
    """
    Check if the given string is a valid YouTube video ID.

    Args:
        video_id: The string to be checked.

    Returns:
        bool: True if the string is a valid YouTube video ID, False otherwise.
    """
    return len(video_id) == 11 and all(
        c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in video_id
    )


def file_type() -> str:
    """
    Prompts the user to choose a file type for download and returns
    the chosen file type as a string.

    Args:
        None

    Returns:
        str: The chosen file type as a string.
    """
    # make the console font to red
    questions = [
        inquirer.List(
            "file_type",
            message="Choose the file type you want to download",
            choices=['Audio', 'Video', CANCEL_PREFIX],
        ),
    ]

    try:
        answer = inquirer.prompt(questions)["file_type"]

    # TypeError: 'NoneType' object is not subscriptable

    except TypeError:
        return ABORTED_PREFIX

    except Exception as error:
        error_console.print(f"Error: {error}")
        sys.exit()

    return answer


def ask_resolution(resolutions: set, sizes) -> str:
    """
    Prompts the user to choose a resolution for download
    and returns the chosen resolution as a string.

    Args:
        resolutions (set): The set of available resolutions.

    Returns:
        str: The chosen resolution as a string.
    """
    # Create a dictionary to relate each size with its resolution
    size_resolution_mapping = dict(zip(resolutions, sizes))

    # Generate the choices for the user prompt
    resolution_choices = [
        f"{size} ~= {resolution}" for size, resolution in size_resolution_mapping.items()
    ] + [CANCEL_PREFIX]

    questions = [
        inquirer.List(
            "resolution",
            message="Choose the resolution you want to download",
            choices=resolution_choices,
        ),
    ]

    try:
        answer = inquirer.prompt(questions)["resolution"]

    except TypeError:
        return ABORTED_PREFIX

    except Exception as error:
        error_console.print(f"Error: {error}")
        sys.exit()

     # Extract the resolution part from the user's choice
    return answer.split(" ~= ")[0]


def ask_rename_file(filename: str) -> str:
    """
    Function to ask the user whether to rename, overwrite, or cancel the file operation.

    Args:
        filename (str): The name of the file.

    Returns:
        str: The user's choice to rename, overwrite, or cancel the file operation.
    """
    console.print(
        f"'{filename}' is already exists, do you want to:", style="info")
    questions = [
        inquirer.List(
            "rename",
            message="Do you want to",
            choices=['Rename it', 'Overwrite it', CANCEL_PREFIX.capitalize()],
        ),
    ]
    return inquirer.prompt(questions)["rename"]


def ask_playlist_video_names(videos):
    note = colored("NOTE:", "cyan")
    select_one = colored("<space>", "red")
    select_all = colored("<ctrl+a>", "red")
    invert_selection = colored("<ctrl+i>", "red")
    restart_selection = colored("<ctrl+r>", "red")

    print(
        f"{note} Press {select_one} to select the videos, {select_all} to select all, {
            invert_selection} to invert selection, and {restart_selection} to restart selection",
    )
    questions = [
        inquirer.Checkbox(
            "names",
            message="Choose the videos you want to download:",
            choices=videos,
        ),
    ]

    try:
        answer = inquirer.prompt(questions)["names"]

    except TypeError:
        return ABORTED_PREFIX

    except Exception as error:
        error_console.print(f"Error: {error}")
        sys.exit()

    return answer


def sanitize_filename(filename: str) -> str:
    """
    Removes characters that are not allowed in filenames.

    Args:
        filename: The filename to be sanitized.

    Returns:
        str: The sanitized filename.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def rename_file(filename: str, new_filename: str) -> str:
    """
    Rename a file to a new filename.

    If the new filename does not have the same file extension as the original
    filename, the extension of the original filename will be appended to the
    new filename.

    Args:
        filename: The original filename.
        new_filename: The new filename to rename to.

    Returns:
        str: The new filename after the renaming operation.
    """
    try:
        if not new_filename.endswith(os.path.splitext(filename)[1]):
            new_filename += f".{filename.split('.')[-1]}"
    except IndexError as error:
        error_console.print(f"Error: {error}")
        sys.exit()
    return new_filename


def is_file_exists(path: str, filename: str) -> bool:
    """
    Check if a file exists at the specified path and filename.

    Args:
        path: The path where the file is located.
        filename: The name of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(os.path.join(path, filename))


def check_for_updates() -> None:
    """
    A function to check for updates of a given package.

    Returns:
        None
    """
    try:
        r = requests.get(
            f'https://pypi.org/pypi/{__app__}/json', headers={'Accept': 'application/json'})
    except Exception as error:
        error_console.print(f"❗ Error checking for updates: {error}")
    else:
        if r.status_code == 200:
            latest_version = r.json()['info']['version']

            if latest_version != __version__:
                console.print(
                    f"👉 A new version of {__app__} is available: {
                        latest_version}. Update it by running [bold red link=https://github.com/Hetari/pyutube]pip install --upgrade {__app__}[/bold red link]",
                    style="warning"
                )
        else:
            error_console.print(
                f"❗ Error checking for updates: {r.status_code}")
            sys.exit()

# main utils


def check_internet_connection() -> bool:
    """
    Checks if an internet connection is available.

    Returns:
        bool: True if internet connection is available, False otherwise.
    """
    if not is_internet_available():
        error_console.print("❗ No internet connection")
        return False

    console.print("✅ There is internet connection", style="info")
    console.print()
    return True


def validate_link(url: str) -> tuple[bool, str]:
    """
    Validates the given YouTube video URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating if the link is valid
        and a string indicating the type of the link (video or short).
    """
    is_valid_link, link_type = is_youtube_link(url)
    if not is_valid_link:
        console.print("❌ Invalid link", style="danger")

    return is_valid_link, link_type.lower()


def handle_video_link() -> bool:
    """
    Handles video link scenario.

    Args:
        None

    Returns:
        bool: True if the video link is valid, False otherwise.
    """
    file_type_choice = file_type().lower()
    is_audio = file_type_choice.startswith("audio")

    if file_type_choice.startswith(CANCEL_PREFIX):
        error_console.print("❗ Cancel the download...")
        sys.exit()
    elif file_type_choice.startswith(ABORTED_PREFIX):
        sys.exit()

    return is_audio
