"""
This module contains the Downloader class which provides functionality
for downloading videos from YouTube.
"""


class Downloader:
    """
    This class provides functionality for downloading videos from YouTube.
    """

    def __init__(
            self,
            url: str,
            path: str,
            quality: str,
            is_audio: bool = False,
    ):
        """
            Initializes a Downloader object.

            Args:
                url: The URL of the video or playlist to download.
                path: The path where the downloaded file(s) will be saved.
                quality: The desired quality of the video, default is None.
                is_audio: Flag indicating if the video should be downloaded
                    as audio, default is False.

        """
