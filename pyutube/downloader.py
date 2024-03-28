from yaspin import yaspin
from yaspin.spinners import Spinners
from pytube import YouTube
from pytube.cli import on_progress
from termcolor import colored
import ffmpeg

import os
import subprocess

from .utils import (
    clear,
    console,
    error_console,
    sanitize_filename,
    ask_rename_file,
    ask_resolution,
    rename_file,
    is_file_exists,
)


class Downloader:
    def __init__(self, url: str, path: str, is_audio: bool = False, is_playlist: bool = False, is_short: bool = False):
        self.url = url
        self.path = path
        self.quality = "720p"
        self.is_audio = is_audio
        self.is_playlist = is_playlist
        self.is_short = is_short

    @yaspin(text=colored("Searching for the video", "green"), color="green", spinner=Spinners.point)
    def video_search(self, url: str) -> YouTube:
        """
        This function searches for a video using the provided URL and returns an
        instance of the YouTube class representing the searched video.

        Args:
            url: The URL of the video to search for.

        Returns:
            YouTube: An instance of the YouTube class representing the searched video.
        """

        return YouTube(
            url,
            use_oauth=False,
            allow_oauth_cache=True,
            on_progress_callback=on_progress,
        )

    @yaspin(text=colored("getting video headers ", "green") + colored("(means the video won't be fully downloaded)", "yellow"), spinner=Spinners.point)
    def get_available_resolutions(self, video: YouTube) -> set:
        """
        Get a set of all available resolutions for the video.

        Args:
            video: The video to retrieve available resolutions from.

        Returns:
            set: A set containing all available resolutions.
        """
        streams = video.streams

        available_streams = streams.filter(
            progressive=False, adaptive=True, mime_type="video/mp4")

        audio_stream = streams.filter(
            only_audio=True).order_by('mime_type').first()

        resolutions_with_sizes = self.get_video_resolutions_sizes(
            available_streams, audio_stream
        )

        resolutions_with_sizes = sorted(
            resolutions_with_sizes, key=lambda x: int(
                x[0][:-1]) if x[0][:-1].isdigit() else float('inf')
        )

        # Separate resolutions and sizes without using two loops
        resolutions, sizes = zip(*resolutions_with_sizes)
        resolutions = list(resolutions)
        sizes = list(sizes)

        return resolutions, sizes, available_streams, audio_stream

    @yaspin(text=colored("Downloading the video...", "green"), color="green", spinner=Spinners.dots13)
    def get_video_streams(self, quality: str, streams: YouTube.streams) -> YouTube:
        """
        Downloads the video streams based on the specified quality.
        If the specified quality is not available, it selects the nearest quality.

        Args:
            video: The video to retrieve streams from.
            quality: The desired quality of the video streams.

        Returns:
            The video stream with the specified quality, or the best available stream if no match is found.
        """
        return streams.filter(res=quality).first()

    @yaspin(text=colored("Downloading the audio...", "green"), color="green", spinner=Spinners.dots13)
    def get_audio_streams(self, video: YouTube) -> YouTube:
        """
        Function to get audio streams from a video.

        Args:
            video: The video for which audio streams are to be obtained.

        Returns:
            The first audio stream found in the video.
        """
        return video.streams.filter(only_audio=True).order_by('mime_type').first()

    @yaspin(text=colored("Saving the file...", "cyan"), spinner=Spinners.smiley)
    def save_file(self, video: YouTube, path: str, filename: str) -> None:
        """
        Save the file to the specified path with the given filename.

        Args:
            video: The video to be saved.
            path: The path where the video will be saved.
            filename: The name of the file.

        Returns:
            None
        """
        video.download(output_path=path, filename=filename)

    # Helper functions for the Downloader class
    def search_process(self) -> YouTube:
        try:
            video = self.video_search(self.url)
        except Exception as error:
            error_console.print(f"Error: {error}")
            return False

        # If video is not found
        if not video:
            error_console.print(
                f"No {'audio' if self.is_audio else 'video'} stream available for the video.")
            return False

        console.print(f"Title: {video.title}\n", style="info")
        return video

    def get_selected_stream(self, video):
        """
        Get the selected video stream based on user preference.

        Returns:
            YouTube: The selected video stream.
        """
        resolutions, sizes,  streams, video_audio = self.get_available_resolutions(
            video)
        self.quality = ask_resolution(resolutions, sizes)

        return [] if self.quality.startswith("cancel") else streams, video_audio

    def generate_filename(self, video, video_id):
        """
        Generate a filename for the downloaded video.

        Returns:
            str: The generated filename.
        """
        quality = 'audio' if self.is_audio else video.resolution
        title = sanitize_filename(video.title)
        return f"{title} - {quality}_-_{video_id}.{'mp3' if self.is_audio else video.mime_type.split('/')[1]}"

    def handle_existing_file(self, filename):
        """
        Handle the case where a file with the same name already exists.

        Returns:
            str: The user's choice.
        """
        choice = ask_rename_file(filename).lower()
        if choice.startswith('rename'):
            filename = self.prompt_new_filename(filename)
            if not filename:
                error_console.print("Invalid filename")
                return False
            return filename
        elif choice.startswith('cancel'):
            console.print("Download canceled", style="info")
            return False
        return True

    def prompt_new_filename(self, filename):
        """
        Prompt the user for a new filename.

        Returns:
            str: The new filename.
        """
        text = colored(filename, 'yellow')
        new_name = input(f"Rename {text} to: ")
        return rename_file(filename, new_name)

    def merging(self, video_name: str, audio_name: str, video_id: str):
        output_directory = "output"
        os.makedirs(output_directory, exist_ok=True)

        # Merge video and audio using ffmpeg-python
        input_video = ffmpeg.input(video_name)
        input_audio = ffmpeg.input(audio_name)

        # Build FFmpeg command string
        ffmpeg_command = ffmpeg.output(
            ffmpeg.concat(input_video, input_audio, v=1, a=1),
            f'{output_directory}/{video_name}').compile()

        # Run FFmpeg command using subprocess
        try:
            subprocess.run(ffmpeg_command, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            print('An error occurred:', e.stderr)
        else:
            os.remove(video_name)
            os.remove(audio_name)

            output_file = os.path.join(output_directory, video_name)

            if os.path.exists(output_file):
                os.replace(output_file, os.path.join(os.getcwd(), video_name))
                os.rmdir(output_directory)
            else:
                print("Merged video file not found in the output directory.")

    @staticmethod
    def get_video_resolutions_sizes(available_streams: list[YouTube], audio_stream: YouTube) -> list:
        """
        Get the available video resolutions.

        Args:
            available_streams: The available video streams.
            audio_stream: The audio stream.

        Returns:
            list: The available video resolutions.
        """
        if not available_streams:
            return []

        # Calculate the total audio file size in bytes
        audio_filesize_bytes = audio_stream.filesize_approx

        # Convert the audio file size to KB
        audio_filesize_kb = audio_filesize_bytes / 1000

        resolutions_with_sizes = []
        for stream in available_streams:
            if stream.resolution:
                # Calculate the total video file size including audio in bytes
                video_filesize_bytes = stream.filesize_approx + \
                    (2 * audio_filesize_bytes)
                # Convert the video file size to KB or MB dynamically
                if video_filesize_bytes >= 1024 * 1024:
                    # If size is >= 1 MB
                    video_filesize = \
                        f"{video_filesize_bytes / (1024 * 1024):.2f} MB"
                else:
                    video_filesize = f"{video_filesize_bytes / 1024:.2f} KB"

                resolutions_with_sizes.append(
                    (stream.resolution, video_filesize))

        return resolutions_with_sizes

    def download_video(self):
        """
        Download a video from a given URL to a specified path.

        Args:
            url: The URL of the video.
            path: The path to save the downloaded video.
            quality: The quality of the video, default is '720p'.
            is_audio: Flag indicating if the video should be downloaded as audio, default is False.

        Returns:
            bool: True if the video is downloaded successfully, False otherwise.
        """
        video = self.search_process()

        if not video:
            return False

        video_id = video.video_id

        if self.is_audio:
            footage = self.get_audio_streams(video)

        else:
            # shorts and videos
            streams, video_audio = self.get_selected_stream(video)

            if not streams:
                error_console.print("❗ Cancel the download...")
                return
            footage = self.get_video_streams(self.quality, streams)

            # Generate filename with title, quality, and file extension
            self.is_audio = True
            audio_filename = self.generate_filename(video_audio, video_id)
            self.is_audio = False

        if not footage:
            error_console.print(
                "Something went wrong while downloading the video.")
            return False

        video_filename = self.generate_filename(footage, video_id)

        # If file with the same name already exists in the path
        if is_file_exists(self.path, video_filename):
            video_filename = self.handle_existing_file(video_filename)
            if not video_filename:
                return False
        try:
            self.save_file(footage, self.path, video_filename)
            if not self.is_audio:
                self.save_file(video_audio, self.path, audio_filename)
                self.merging(video_filename, audio_filename, video_id)

        except Exception as error:
            error_console.print(f"Error: {error}")
            return False

        console.print("✅ Download completed", style="info")
        return True


def download(url: str, path: str, is_audio: bool) -> None:
    """
    Downloads the YouTube video based on the provided parameters.

    Args:
        url (str): The URL of the YouTube video.
        path (str): The path to save the video.
        quality_choice (str): The chosen quality for the video.
        is_audio (bool): Whether the download is for audio.

    Returns:
        None
    """
    downloader = Downloader(
        url=url, path=path, is_audio=is_audio,
    )
    downloader.download_video()
    del downloader
