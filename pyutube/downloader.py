"""
This module contains the Downloader class which provides functionality 
for downloading videos from YouTube.
"""
from .utils import (
    console,
    error_console,
    sanitize_filename,
    ask_rename_file,
    ask_resolution,
    rename_file,
    is_file_exists,
    CANCEL_PREFIX
)

import os
import sys


from yaspin import yaspin
from yaspin.spinners import Spinners
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from termcolor import colored
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio


class Downloader:
    """
    This class provides functionality for downloading videos from YouTube.
    """

    def __init__(
            self,
            url: str,
            path: str,
            quality: None = None,
            is_audio: bool = False,
            is_playlist: bool = False,
    ):
        """
            Initializes a Downloader object.

            Args:
                url: The URL of the video or playlist to download.
                path: The path where the downloaded file(s) will be saved.
                quality: The desired quality of the video, default is None.
                is_audio: Flag indicating if the video should be downloaded 
                    as audio, default is False.
                is_playlist: Flag indicating if the URL is for a playlist, default is False.
        """
        self.url = url
        self.path = path
        self.quality = quality
        self.is_audio = is_audio
        self.is_playlist = is_playlist

    @yaspin(
        text=colored("Searching for the video", "green"),
        color="green", spinner=Spinners.point
    )
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

    @yaspin(
        text=colored("getting video streams", "green"),
        spinner=Spinners.point
    )
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

    @yaspin(
        text=colored("Downloading the video...", "green"),
        color="green", spinner=Spinners.dots13
    )
    def get_video_streams(self, quality: str, streams: YouTube.streams) -> YouTube:
        """
        Downloads the video streams based on the specified quality.
        If the specified quality is not available, it selects the nearest quality.

        Args:
            video: The video to retrieve streams from.
            quality: The desired quality of the video streams.

        Returns:
            The video stream with the specified quality, 
            or the best available stream if no match is found.
        """
        s = streams.filter(res=quality).first()

        if not s:
            available_qualities = [stream.resolution for stream in streams]
            available_qualities = list(map(int, available_qualities))
            selected_quality = min(available_qualities,
                                   key=lambda x: abs(int(quality) - x))
            s = streams.filter(res=str(selected_quality)).first()

        return s

    @yaspin(
        text=colored("Downloading the audio...", "green"),
        color="green",
        spinner=Spinners.dots13
    )
    def get_audio_streams(self, video: YouTube) -> YouTube:
        """
        Function to get audio streams from a video.

        Args:
            video: The video for which audio streams are to be obtained.

        Returns:
            The first audio stream found in the video.
        """
        return video.streams.filter(only_audio=True).order_by('mime_type').first()

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
        """
        Performs the video search process.

        Returns:
            YouTube: An instance of the YouTube class representing the searched video.
        """
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
        self.quality = ask_resolution(
            resolutions, sizes) if self.quality is None else self.quality

        return [] if self.quality.startswith(CANCEL_PREFIX) else streams, video_audio

    def generate_filename(self, video, video_id):
        """
        Generate a filename for the downloaded video.

        Returns:
            str: The generated filename.
        """
        quality = 'audio' if self.is_audio else video.resolution
        title = video.default_filename
        extension = 'mp3' if self.is_audio else video.mime_type.split('/')[1]

        return f"{title} - {quality}_-_{video_id}.{extension}"

    def handle_existing_file(self, filename):
        """
        Handle the case where a file with the same name already exists.

        Returns:
            str: The user's choice.
        """
        choice = ask_rename_file(filename).lower()
        if choice.startswith('rename'):
            filename = sanitize_filename(
                self.prompt_new_filename(filename)
            )
            if not filename:
                error_console.print("Invalid filename")
                return False
            return filename
        elif choice.startswith('cancel'):
            console.print("Download canceled", style="info")
            return False

        # else overwrite
        return filename

    def prompt_new_filename(self, filename):
        """
        Prompt the user for a new filename.

        Returns:
            str: The new filename.
        """
        text = colored(filename, 'yellow')
        new_name = input(f"Rename {text} to: ")
        return rename_file(filename, new_name)

    def merging(self, video_name: str, audio_name: str):
        """
        Merges the video and audio files into a single file.

        Args:
            video_name: The name of the video file.
            audio_name: The name of the audio file.
            video_id: The ID of the video.

        Returns:
            None
        """

        output_directory = os.path.join(self.path, "output")
        os.makedirs(output_directory, exist_ok=True)
        output_file = os.path.join(
            output_directory, os.path.basename(video_name))

        ffmpeg_merge_video_audio(
            video_name,
            audio_name,
            output_file,
            vcodec='copy',
            acodec='copy',
            ffmpeg_output=False,
            logger=None
        )

        # Remove original files
        os.remove(video_name)
        os.remove(audio_name)

        # Move the merged file to the current directory
        if os.path.exists(output_file):
            os.replace(output_file, os.path.join(os.getcwd(), video_name))
            os.rmdir(output_directory)
        else:
            error_console.print(
                "Merged video file not found in the output directory.")

    @staticmethod
    def get_video_resolutions_sizes(
            available_streams: list[YouTube],
            audio_stream: YouTube
    ) -> list:
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
        audio_filesize = audio_stream.filesize

        resolutions_with_sizes = []
        one_mb = 1024 * 1024
        one_gb = one_mb * 1024
        for stream in available_streams:
            if stream.resolution:
                # Calculate the total video file size including audio in bytes
                video_filesize_bytes = stream.filesize

                if not stream.is_progressive:
                    video_filesize_bytes += audio_filesize

                # Convert the video file size to KB or MB dynamically
                if video_filesize_bytes >= one_gb:
                    # If size is >= 1 GB
                    video_filesize = \
                        f"{video_filesize_bytes / (one_gb):.4f} GB"

                elif video_filesize_bytes >= one_mb:
                    # If size is >= 1 MB
                    video_filesize = \
                        f"{video_filesize_bytes / (one_mb):.2f} MB"
                else:
                    video_filesize = f"{video_filesize_bytes / 1024:.2f} KB"

                resolutions_with_sizes.append(
                    (stream.resolution, video_filesize))

        return resolutions_with_sizes

    def download_video(self) -> bool:
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
            error_console.print("❗ The video could not be found.")
            sys.exit()

        video_id = video.video_id

        if self.is_audio:
            footage = self.get_audio_streams(video)

        else:
            # shorts and videos
            streams, video_audio = self.get_selected_stream(video)

            if not streams or self.quality.startswith(CANCEL_PREFIX):
                error_console.print("❗ Cancel the download...")
                sys.exit()

            footage = self.get_video_streams(self.quality, streams)

            # Generate filename with title, quality, and file extension
            self.is_audio = True
            audio_filename = self.generate_filename(video_audio, video_id)
            audio_filename = os.path.join(self.path, audio_filename)

            self.is_audio = False

        if not footage:
            error_console.print(
                "Something went wrong while downloading the video.")
            sys.exit()

        video_filename = self.generate_filename(footage, video_id)
        video_filename = os.path.join(self.path, video_filename)

        # If file with the same name already exists in the path
        if is_file_exists(self.path, video_filename):
            video_filename = self.handle_existing_file(video_filename)
            if not video_filename:
                sys.exit()
        try:
            console.print(
                f"⏳ Downloading {'audio' if self.is_audio else 'video'}...", style="info")

            self.save_file(footage, self.path, video_filename)

            if not self.is_audio:
                self.save_file(video_audio, self.path, audio_filename)
                self.merging(video_filename, audio_filename)

        except Exception as error:
            error_console.print(f"Error: {error}")
            sys.exit()

        console.print("\n\n\n✅ Download completed", style="info")
        return True

    def get_playlist_links(self):
        """
        Get the playlist links from the URL.

        Args:
            url (str): The URL of the YouTube playlist.

        Returns:
            list: A list of playlist links.
        """
        return Playlist(self.url)


def download(
    url: str,
    path: str,
    is_audio: bool,
    is_playlist: bool = False,
    quality_choice: str = None
) -> None:
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
        url=url, path=path, quality=quality_choice, is_audio=is_audio, is_playlist=is_playlist
    )

    if is_playlist:
        return downloader.get_playlist_links()

    downloader.download_video()

    return downloader.quality
