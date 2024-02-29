# Logic for downloading YouTube videos
import os
import pytube
from pytube import YouTube
from rich.progress import track

PATH = os.getcwd()


def download_video(url, quality='720p', path=PATH):
    youtube = YouTube(
        url, use_oauth=False, allow_oauth_cache=True
    )

    video = youtube.streams.filter(
        res=quality, progressive=True).first()

    try:
        if video:
            title = youtube.title
            filename = f"{title} - {quality}.mp4"
            if os.path.isfile(os.path.join(path, filename)):
                print(f"File {filename} already exists, do you want to:")
                print("[r]ename, [o]verwrite or [c]ancel?")
                choice = input()

                if choice.lower() == 'r':
                    filename = input(f"{filename} Rename to: ")
                elif choice.lower() != 'o':
                    print("Download canceled")
                    return

            video.download(output_path=path, filename=filename)
            print("Download successful!")
        else:
            print(f"No {quality} stream available for the video.")
    except Exception as error:
        print(f"Error: {error}")


def on_progress():
    ...


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=N3CALZudhkI"
    download_video(url)
