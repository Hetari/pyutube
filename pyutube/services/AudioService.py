from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners
from pytubefix import YouTube


class AudioService:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    @yaspin(
        text=colored("Downloading the audio...", "green"),
        color="green",
        spinner=Spinners.dots13
    )
    def get_audio_streams(video: YouTube) -> YouTube:
        """
        Function to get audio streams from a video.

        Args:
            video: The video for which audio streams are to be obtained.

        Returns:
            The first audio stream found in the video.
        """
        return video.streams.filter(only_audio=True).order_by('mime_type').first()
