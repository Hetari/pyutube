# Logic for downloading YouTube videos
import os
from yaspin import yaspin
from yaspin.spinners import Spinners
from pytube import YouTube
from pytube.cli import on_progress
from termcolor import colored
from utils import (
    console,
    error_console,
    sanitize_filename,
    ask_rename_file,
    rename_file,
    is_file_exists,
)

PATH = os.getcwd()


@yaspin(text=colored("Searching for the video", "green"), color="green", spinner=Spinners.point)
def video_search(url: str, quality: str):
    return YouTube(
        url,
        use_oauth=False,
        allow_oauth_cache=True,
        on_progress_callback=on_progress,
    )


@yaspin(text=colored("Downloading the video...", "cyan"), color="cyan", spinner=Spinners.dots13)
def get_video_streams(video, quality):
    return video.streams.filter(res=quality, progressive=True).first() or video.streams.filter(progressive=True).order_by('resolution').first()


@yaspin(text=colored("Saving the video...", "cyan"), spinner=Spinners.smiley)
def save_video(video, path, filename):
    video.download(output_path=path, filename=filename)


def download_video(url, quality='720p', path=PATH):
    try:
        video = video_search(url, quality)
    except Exception as error:
        error_console.print(f"Error: {error}")
        return False

    if not video:
        error_console.print(
            f"No {quality} stream available for the video.")
        return False

    video = get_video_streams(video, quality)

    quality = video.resolution
    title = sanitize_filename(video.title)
    filename = f"{title} - {quality}.mp4"

    if is_file_exists(path, filename):
        choice = ask_rename_file(filename)

        if choice.lower().startswith('r'):
            text = colored(filename, 'yellow')
            new_name = input(f"Rename {text} to: ")
            filename = rename_file(filename, new_name)

            if not filename:
                error_console.print("Invalid filename")
                return False

        elif choice.lower().startswith('c'):
            console.print("Download canceled", style="info")
            return False
    try:
        save_video(video, path, filename)

    except Exception as error:
        error_console.print(f"Error: {error}")
        return False

    return True


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=N3CALZudhkI"
    # url = "https://www.youtube.com/watch?v=lukT_WB5IB0"
    # url = "https://www.youtube.com/watch?v=o9mJFqqgG88"
    # test_download("https://www.youtube.com/watch?v=N3CALZudhkI")
    download_video(url, quality="240p")
