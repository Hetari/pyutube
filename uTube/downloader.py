# Logic for downloading YouTube videos
from functools import wraps
import os
from pytube import YouTube
from pytube.cli import on_progress
from utils import (
    console,
    error_console,
    sanitize_filename,
    ask_rename_file,
    rename_file
)

PATH = os.getcwd()


def download_video(url, quality='720p', path=PATH):
    youtube = YouTube(
        url, use_oauth=False, allow_oauth_cache=True, on_progress_callback=on_progress
    )

    video = youtube.streams.filter(
        res=quality, progressive=True)

    video = video.first()

    try:
        if video:
            print(f"Downloading {quality} stream...")
            title = sanitize_filename(youtube.title)
            filename = f"{title} - {quality}.mp4"

            if os.path.isfile(os.path.join(path, filename)):
                choice = ask_rename_file(filename)
                if choice.lower().startswith('r'):
                    new_name = input(f"{filename} Rename to: ")
                    filename = rename_file(filename, new_name)
                    if not filename:
                        error_console.print("Invalid filename")
                        return False

                elif choice.lower() != 'o':
                    console.print("Download canceled", style="info")
                    return False

            video.download(output_path=path, filename=filename)
        else:
            error_console.print(
                f"No {quality} stream available for the video.")
            return False
    except Exception as error:
        error_console.print(f"Error: {error}")
        return False

    return True


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=N3CALZudhkI"
    # url = "https://www.youtube.com/watch?v=lukT_WB5IB0"
    download_video(url)
    # test_download("https://www.youtube.com/watch?v=N3CALZudhkI")
