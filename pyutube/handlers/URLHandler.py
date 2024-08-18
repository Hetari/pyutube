import re
import sys
from pyutube.utils import console, error_console


class URLHandler:
    def __init__(self, url):
        self.url = url

    def validate(self):
        if self.__is_youtube_video_id(self.url):
            self.url = f"https://www.youtube.com/watch?v={self.url}"

        return self.__validate_link(self.url)

    def __validate_link(self, url: str) -> tuple[bool, str]:
        """
        Validates the given YouTube video URL.

        Args:
            url (str): The URL of the YouTube video.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating if the link is valid
            and a string indicating the type of the link (video or short).
        """
        is_valid_link, link_type = self.__is_youtube_link(url)
        if not is_valid_link:
            error_console.print("❌ Invalid link")
            sys.exit(1)

        return is_valid_link, link_type.lower()

    def __is_youtube_link(self, link: str) -> tuple[bool, str]:
        """
        Check if the given link is a YouTube video, playlist, or shorts link.

        Args:
            link (str): The link to be checked.

        Returns:
            tuple[bool, str]: True if the link is a YouTube video, playlist, or shorts link,
            False otherwise. The second item of the tuple indicates the type of link found:
            'video', 'playlist', or 'shorts'.
        """
        is_video = self.__is_youtube_video(link)
        is_short = self.__is_youtube_shorts(link)
        is_playlist = self.__is_youtube_playlist(link)

        return (is_video, "video") if is_video \
            else (is_short, "short") if is_short \
            else (True, "playlist") if is_playlist\
            else (False, "unknown")

    def __is_youtube_shorts(self, link: str) -> bool:
        """
        Check if the given link is a YouTube shorts link.

        Args:
            link: The link to be checked.

        Returns:
            bool: True if the link is a YouTube shorts link, False otherwise.
        """
        # shorts_pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]+)"
        shorts_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|shorts\/|watch\?.*?v=))(?:(?:[^\/\n\s]+\/)?)([a-zA-Z0-9_-]+)"
        shorts_match = re.match(shorts_pattern, link)
        return bool(shorts_match)

    def __is_youtube_video(self, link: str) -> bool:
        """
        Check if the given link is a YouTube video.

        Args:
            link: The link to be checked.

        Returns:
            bool: True if the link is a YouTube video, False otherwise.
        """
        # video_pattern = re.compile(
        # r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:(?:live/?[a-zA-Z0-9_-]{11}\?si=)|(?:(?:watch\?v=)|(?:embed/))|youtu\.be/|youtube.com/share\?v=)([a-zA-Z0-9_-]{11}))')
        # video_pattern = re.compile(
        # r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:(?:watch\?v=)|(?:embed/))|youtu\.be/|youtube.com/share\?v=)([a-zA-Z0-9_-]{11})')
        video_pattern = re.compile(
            # "https://www.youtube.com/watch?time_continue=1&v=dQw4w9WgXcQ"
            r"^(?:https?://)?(?:www\.)?(?:youtube(?:-nocookie)?\.com/(?:(watch\?v=|watch\?feature\=share\&v=)|embed/|v/|live_stream\?channel=|live\/)|youtu\.be/)([a-zA-Z0-9_-]{11})"
        )

        return bool(video_pattern.match(link))

    def __is_youtube_playlist(self, link: str) -> bool:
        """
        Check if the given link is a YouTube playlist.

        Args:
            link: The link to be checked.

        Returns:
            bool: True if the link is a YouTube playlist, False otherwise.
        """
        playlist_pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/playlist\?list=([a-zA-Z0-9_-]+)"
        playlist_match = re.match(playlist_pattern, link)
        return bool(playlist_match)

    def __is_youtube_video_id(self, video_id: str) -> bool:
        """
        Check if the given string is a valid YouTube video ID.

        Args:
            video_id: The string to be checked.

        Returns:
            bool: True if the string is a valid YouTube video ID, False otherwise.
        """
        return len(video_id) == 11 and all(
            c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in video_id
        )
