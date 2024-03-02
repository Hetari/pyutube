import re
import inquirer
import requests
import os
from yaspin import yaspin
from yaspin.spinners import Spinners
from rich.console import Console
from rich.theme import Theme
from rich.color import Color


__app_name__: str = "uTube"
__version__: str = "1.0"

custom_theme = Theme({
    "info": "#64b0f2",
    "warning": "color(3)",
    "danger": "red",
    "success": "green",
})

console = Console()
error_console = Console(stderr=True, style="red")
console = Console(theme=custom_theme)


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


@yaspin(text="Checking internet connection", color="blue", spinner=Spinners.earth)
def is_internet_available():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def is_youtube_link(link):
    # Regular expression pattern to match YouTube video URLs
    youtube_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

    # Regular expression pattern to match YouTube playlist URLs
    playlist_pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:playlist|watch)\?(?:.*&)?list=([a-zA-Z0-9_-]+)"

    # Match the pattern against the link for video
    video_match = re.match(youtube_pattern, link)

    # Match the pattern against the link for playlist
    playlist_match = re.match(playlist_pattern, link)

    # If match is found for video or playlist, return True, otherwise return False
    return bool(video_match) or bool(playlist_match)


def file_type() -> dict:
    questions = [
        inquirer.List(
            "file_type",
            message="Do you want to download this link audio or video?",
            choices=['audio', 'video'],
        ),
    ]
    return inquirer.prompt(questions)["file_type"]


def ask_resolution() -> dict:
    questions = [
        inquirer.List(
            "resolution",
            message="Choose the resolution you want to download",
            choices=["144p", "240p", "360p", "480p",
                     "720p", "1080p", "2k", "4k"],
        ),
    ]
    return inquirer.prompt(questions)["resolution"]


def sanitize_filename(filename: str) -> str:
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def ask_rename_file(filename: str) -> str:
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


def rename_file(filename: str, new_filename: str) -> str:
    try:
        if not new_filename.endswith(os.path.splitext(filename)[1]):
            new_filename += f".{filename.split('.')[-1]}"
    except IndexError as error:
        error_console.print(error)
    return new_filename


def is_file_exists(path: str, filename):
    return os.path.isfile(os.path.join(path, filename))
