import os
import sys
from pytubefix import YouTube
from pytubefix.helpers import safe_filename
from termcolor import colored

from pyutube.utils import ask_rename_file, error_console, console


class FileService:

    def save_file(self, video: YouTube, filename: str, path: str) -> None:
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

    def generate_filename(self, video, video_id, is_audio=False, filename: str = ""):
        """
        Generate a filename for the downloaded video.

        Returns:
            str: The generated filename.
        """
        file_type = 'audio' if is_audio else video.resolution

        extension = 'mp3' if is_audio else video.mime_type.split('/')[1]

        title = filename if filename != "" else video.default_filename.split('.')[0]

        return f"{title} - {file_type}_-_{video_id}.{extension}"

    def handle_existing_file(
            self, video: YouTube, video_id: str, filename: str, path: str, is_audio: bool = False) -> None:
        """
        Handle the case where a file with the same name already exists.

        Returns:
            str: The user's choice.
        """
        # If file with the same name already exists in the path
        if not self.is_file_exists(path, filename):
            return filename

        choice = ask_rename_file(filename).lower()
        if choice.startswith('rename'):
            filename = safe_filename(
                self.prompt_new_filename(filename)
            )
            if not filename:
                error_console.print("Invalid filename")
                return False
            filename = self.generate_filename(video, video_id, is_audio, filename)

            return filename
        elif choice.startswith('cancel'):
            console.print("Download canceled", style="info")
            sys.exit()

        # else overwrite
        return filename

    def prompt_new_filename(self, filename):
        """
        Prompt the user for a new filename.

        Returns:
            str: The new filename.
        """
        text = colored(filename, 'yellow')
        return input(f"Rename {text} to: ")

    @staticmethod
    def is_file_exists(path: str, filename: str) -> bool:
        """
        Check if a file exists at the specified path and filename.

        Args:
            path: The path where the file is located.
            filename: The name of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.isfile(os.path.join(path, filename))
