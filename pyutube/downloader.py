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

    @yaspin(text=colored("getting video headers ", "green") + colored("(means the video won't be downloaded)", "yellow"), spinner=Spinners.point)
    def get_available_resolutions(self, video: YouTube) -> set:
        """
        Get a set of all available resolutions for the video.

        Args:
            video: The video to retrieve available resolutions from.

        Returns:
            set: A set containing all available resolutions.
        """
        available_streams = video.streams.filter(progressive=True)
        return {
            stream.resolution for stream in available_streams if stream.resolution
        }, available_streams

    @yaspin(text=colored("Downloading the video...", "green"), color="green", spinner=Spinners.dots13)
    def get_video_streams(self, video: YouTube, quality: str, streams: YouTube.streams) -> YouTube:
        """
        Downloads the video streams based on the specified quality.
        If the specified quality is not available, it selects the nearest quality.

        Args:
            video: The video to retrieve streams from.
            quality: The desired quality of the video streams.

        Returns:
            The video stream with the specified quality, or the best available stream if no match is found.
        """
        available_streams = streams.order_by('resolution')

        return available_streams.get_by_resolution(quality) or available_streams.first()

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

        if self.is_audio:
            file = self.get_audio_streams(video)
        else:
            # shorts and videos
            streams = self.get_selected_stream(video)
            file = self.get_video_streams(video, self.quality, streams)

        if not file:
            error_console.print(
                "Something went wrong while downloading the video.")
            return False

        # Generate filename with title, quality, and file extension
        filename = self.generate_filename(file)

        # If file with the same name already exists in the path
        if is_file_exists(self.path, filename):
            cancel = self.handle_existing_file(filename)
            if not cancel:
                return False
        try:
            self.save_file(file, self.path, filename)

        except Exception as error:
            error_console.print(f"Error: {error}")
            return False

        return True

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
        resolutions, streams = self.get_available_resolutions(video)
        self.quality = ask_resolution(resolutions)
        return streams

    def generate_filename(self, video):
        """
        Generate a filename for the downloaded video.

        Returns:
            str: The generated filename.
        """
        quality = 'audio' if self.is_audio else video.resolution
        title = sanitize_filename(video.title)
        return f"{title} - {quality}.{'mp3' if self.is_audio else video.mime_type.split('/')[1]}"

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
        elif choice.startswith('cancel'):
            console.print("Download canceled", style="info")
            return False

    def prompt_new_filename(self, filename):
        """
        Prompt the user for a new filename.

        Returns:
            str: The new filename.
        """
        text = colored(filename, 'yellow')
        new_name = input(f"Rename {text} to: ")
        return rename_file(filename, new_name)


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
