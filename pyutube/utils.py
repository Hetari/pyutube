import re
import inquirer
import requests
import os
from yaspin import yaspin
from yaspin.spinners import Spinners
from rich.console import Console
from rich.theme import Theme


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
        requests.get(
            "https://www.google.com/webhp?hl=en&sa=X&ved=0ahUKEwi01K6f_-eEAxWnRKQEHYC3AxkQPAgJ", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def is_youtube_link(link: str) -> bool:
    """
    Check if the given link is a YouTube video or playlist link.

    Args:
        link: The link to be checked.

    Returns:
        bool: True if the link is a YouTube video or playlist link, False otherwise.
    """
    # Regular expression pattern to match YouTube video URLs
    youtube_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

    # Regular expression pattern to match YouTube playlist URLs
    # playlist_pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:playlist|watch)\?(?:.*&)?list=([a-zA-Z0-9_-]+)"

    # Match the pattern against the link for video
    video_match = re.match(youtube_pattern, link)

    # Match the pattern against the link for playlist
    # playlist_match = re.match(playlist_pattern, link)

    # If match is found for video or playlist, return True, otherwise return False
    return bool(video_match)


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


def ask_resolution() -> str:
    """
    Prompts the user to choose a resolution for download and returns the chosen resolution as a string.

    Args:
        None

    Returns:
        str: The chosen resolution as a string.
    """
    questions = [
        inquirer.List(
            "resolution",
            message="Choose the resolution you want to download",
            choices=["144p", "240p", "360p", "480p",
                     "720p", "1080p", "Cancel the download"],
        ),
    ]

    try:
        answer = inquirer.prompt(questions)["resolution"]

    except TypeError as error:
        return "Aborted"

    except Exception as error:
        error_console.print(f"Error: {error}")

    return answer


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


if __name__ == "__main__":
    print(is_internet_available())
