import re
import requests
import os
from yaspin import yaspin
from yaspin.spinners import Spinners
from rich.console import Console
from rich.theme import Theme


__app_name__: str = "uTube"
__version__: str = "1.0"

custom_theme = Theme({
    "info": "#64b0f2",
    "warning": "color(3)",
    "danger": "red",
    "success": "green",
})

console = Console()
console = Console(theme=custom_theme)


def clear():
    print(os.name)
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def welcome():
    console.print(f"Welcome to {__app_name__} v {__version__}", style="info")


@yaspin(text="Checking internet connection", color="blue", spinner=Spinners.earth)
def is_internet_available():
    try:
        requests.get("http://www.google.com", timeout=3)
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
