"""
This module contains the utils functions for the pyutube package.
"""

import sys
import os

import inquirer
import requests
from yaspin import yaspin
from yaspin.spinners import Spinners
from rich.console import Console
from rich.theme import Theme
from termcolor import colored


__version__ = "1.3.24"
__app__ = "pyutube"
ABORTED_PREFIX = "Aborted"
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

    print((
        f"{note} Press {select_one} to select the videos, {select_all} to select all, "
        f"{invert_selection} to invert selection, and {restart_selection} to restart selection"
    ))

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
            if latest_version != __version__ and latest_version < __version__:
                console.print(
                    f"👉 A new version of {__app__}  is available: {latest_version} " +
                    "Update it by running [bold red link=https://github.com/Hetari/pyutube]pip install --upgrade " +
                    f"{__app__}[/bold red link]",
                    style="warning")
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


def asking_video_or_audio() -> bool:
    """
    Handles video link scenario.

    Args:
        None

    Returns:
        bool: True if the video link is valid, False otherwise.
    """
    file_type_choice = file_type().lower()
    is_audio = file_type_choice.startswith("audio")

    if file_type_choice.startswith(CANCEL_PREFIX.lower()):
        error_console.print("❗ Cancel the download...")
        sys.exit()

    return is_audio
