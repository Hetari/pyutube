from yaspin import yaspin
from yaspin.spinners import Spinners
from pytube import YouTube
from pytube.cli import on_progress
from termcolor import colored
from .utils import (
    console,
    error_console,
    sanitize_filename,
    ask_rename_file,
    rename_file,
    is_file_exists,
)


class Downloader:
    def __init__(self, url: str, path: str, quality: str, is_audio: bool = False, is_playlist: bool = False, is_short: bool = False):
        self.url = url
        self.path = path
        self.quality = quality
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

    @yaspin(text=colored("Downloading the video...", "green"), color="green", spinner=Spinners.dots13)
    def get_video_streams(self, video: YouTube, quality: str) -> YouTube:
        """
        Downloads the video streams based on the specified quality.
        If the specified quality is not available, it selects the nearest quality.

        Args:
            video: The video to retrieve streams from.
            quality: The desired quality of the video streams.

        Returns:
            The video stream with the specified quality, or the best available stream if no match is found.
        """
        available_streams = video.streams.filter(
            progressive=True).order_by('resolution')

        # Check if the desired quality is available
        if quality in [stream.resolution for stream in available_streams]:
            return available_streams.get_by_resolution(quality)

        # If the desired quality is not available, find the nearest quality
        # finding the closest resolution to the desired quality
        nearest_quality = None
        min_diff = float('inf')

        for stream in available_streams:
            diff = abs(int(stream.resolution[:-1]) - int(quality[:-1]))
            if diff < min_diff:
                min_diff = diff
                nearest_quality = stream.resolution

        return available_streams.get_by_resolution(nearest_quality)

    @yaspin(text=colored("Downloading the audio...", "green"), color="green", spinner=Spinners.dots13)
    def get_audio_streams(self, video: YouTube) -> YouTube:
        """
        Function to get audio streams from a video.

        Args:
            video: The video for which audio streams are to be obtained.

        Returns:
            The first audio stream found in the video.
        """
        return video.streams.filter(
            only_audio=True).order_by('mime_type').first()

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
        try:
            # Search for the video
            video = self.video_search(self.url)
        except Exception as error:
            error_console.print(f"Error: {error}")
            return False

        # If video is not found
        if not video:
            if not self.is_audio:
                error_console.print(
                    f"No {quality} stream available for the video.")
            else:
                error_console.print(
                    "No audio stream available for the video.")
            return False

        if self.is_audio:
            video = self.get_audio_streams(video)
        else:
            video = self.get_video_streams(video, self.quality)

        # If video stream is not available, imagine that
        if not video:
            error_console.print(
                f"No {quality} stream available for the video.")
            return False

        # Set quality to 'audio' if downloading as audio, otherwise use the video resolution.
        quality = 'audio' if self.is_audio else video.resolution

        # Sanitize video title for use as filename
        title = sanitize_filename(video.title)

        # Generate filename with title, quality, and file extension
        filename = f"{title} - {quality}.{'mp3' if self.is_audio else video.mime_type.split('/')[1]}"

        # If file with the same name already exists in the path
        if is_file_exists(self.path, filename):
            # Ask user if they want to rename the file, overwrite it, or cancel the download process
            choice = ask_rename_file(filename).lower()

            # If user chooses to rename, prompt for new filename
            if choice.startswith('rename'):
                # Color the filename text so it's easier to read in the terminal
                text = colored(filename, 'yellow')
                new_name = input(f"Rename {text} to: ")
                filename = rename_file(filename, new_name)

                if not filename:
                    error_console.print("Invalid filename")
                    return False

            # If user chooses to cancel download
            elif choice.startswith('c'):
                console.print("Download canceled", style="info")
                return False
        try:
            # Attempt to save the video to the specified path with the generated filename
            self.save_file(video, self.path, filename)

        except Exception as error:
            error_console.print(f"Error: {error}")
            return False

        # Return True upon successful download.
        return True
