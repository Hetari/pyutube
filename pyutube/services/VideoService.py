import os
import sys

from yaspin import yaspin
from yaspin.spinners import Spinners
from pytubefix import YouTube
from pytubefix.cli import on_progress
from termcolor import colored
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio

from pyutube.utils import (
    console,
    error_console,
    ask_resolution,
    CANCEL_PREFIX
)


class VideoService:
    def __init__(self, url: str, quality: str, path: str) -> None:
        self.url = url
        self.quality = quality
        self.path = path

    # Helper functions for the Downloader class

    def search_process(self) -> YouTube:
        """
        Performs the video search process.

        Returns:
            YouTube: An instance of the YouTube class representing the searched video.
        """
        try:
            video = self.__video_search()
        except Exception as error:
            error_console.print(f"Error: {error}")
            sys.exit(1)

        if not video:
            error_console.print("No stream available for the url.")
            sys.exit()
        return video

    @staticmethod
    def _print_video_info(video: YouTube) -> None:
        console.print(f"Title: {video.title}\n", style="info")

    @yaspin(
        text=colored("Searching for the video", "green"),
        color="green", spinner=Spinners.point
    )
    def __video_search(self) -> YouTube:
        return YouTube(
            self.url,
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
        stream = streams.filter(res=quality).first()

        if quality.startswith(CANCEL_PREFIX):
            error_console.print("❗ Cancel the download...")
            sys.exit()

        if not stream:
            available_qualities = [stream.resolution for stream in streams]
            available_qualities = list(map(int, available_qualities))
            selected_quality = min(available_qualities,
                                   key=lambda x: abs(int(quality) - x))
            stream = streams.filter(res=str(selected_quality)).first()

        return stream

    def get_selected_stream(self, video, is_audio: bool = False):
        """
        Get the selected video stream based on user preference.

        Returns:
            YouTube: The selected video stream.
        """
        resolutions, sizes,  streams, video_audio = self.get_available_resolutions(
            video)

        if not streams:
            error_console.print("❗ Cancel the download...")
            sys.exit()

        if not is_audio:
            self.quality = self.quality or ask_resolution(resolutions, sizes)

        if not self.quality and not is_audio:
            error_console.print("❗ Cancel the download...")
            sys.exit()

        # TODO:
        # [] if self.quality.startswith(CANCEL_PREFIX) else
        # return streams, video_audio

        return streams, video_audio, self.quality

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
