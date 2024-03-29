import inquirer
import requests
from yaspin import yaspin
from yaspin.spinners import Spinners
from rich.console import Console
from rich.theme import Theme

import re
import os


__version__ = "1.1.5"
ABORTED_PREFIX = "aborted"
CANCEL_PREFIX = "cancel"

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
    Checks if internet connection is available by making a simple request to http://www.google.com with a timeout of 5 seconds.

    Returns:
        bool: the request status (True if available, False if not).
    """
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
    except requests.ReadTimeout:
        return False
    except requests.HTTPError:
        return False
    except requests.TooManyRedirects:
        return False
    except requests.RequestException:
        return False
    except Exception as error:
        error_console.print(f"Error: {error}")
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

    return (is_video, "video") if is_video else (is_short, "short") if is_short else (True, "playlist") if is_playlist else (False, "unknown")


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
    #     r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:(?:watch\?v=)|(?:embed/))|youtu\.be/)([a-zA-Z0-9_-]{11})')

    video_pattern = re.compile(
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:(?:watch\?v=)|(?:embed/))|youtu\.be/|youtube.com/share\?v=)([a-zA-Z0-9_-]{11})')

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
    return len(video_id) == 11 and all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in video_id)


def file_type() -> str:
    """
    Prompts the user to choose a file type for download and returns the chosen file type as a string.

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
            choices=['Audio', 'Video', "Cancel the download"],
        ),
    ]

    try:
        answer = inquirer.prompt(questions)["file_type"]

    # TypeError: 'NoneType' object is not subscriptable

    except TypeError as error:
        return "Aborted"

    except Exception as error:
        error_console.print(f"Error: {error}")

    return answer


def ask_resolution(resolutions: set, sizes) -> str:
    """
    Prompts the user to choose a resolution for download and returns the chosen resolution as a string.

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
    ] + ["Cancel the download"]

    questions = [
        inquirer.List(
            "resolution",
            message="Choose the resolution you want to download",
            choices=resolution_choices,
        ),
    ]

    try:
        answer = inquirer.prompt(questions)["resolution"]

    except TypeError as error:
        return "Aborted"

    except Exception as error:
        error_console.print(f"Error: {error}")

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
            choices=['Rename it', 'Overwrite it', "Cancel"],
        ),
    ]
    return inquirer.prompt(questions)["rename"]


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
    else:
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


def handle_video_link(url: str, path: str) -> None:
    """
    Handles video link scenario.

    Args:
        url (str): The URL of the YouTube video.
        path (str): The path to save the video.

    Returns:
        None
    """
    file_type_choice = file_type().lower()
    is_audio = file_type_choice.startswith("audio")

    if file_type_choice.startswith(CANCEL_PREFIX):
        error_console.print("❗ Cancel the download...")
        return
    elif file_type_choice.startswith(ABORTED_PREFIX):
        return

    return is_audio
