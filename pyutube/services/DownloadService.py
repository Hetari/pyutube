from pyutube.handlers.PlaylistHandler import PlaylistHandler
import os
import sys

from pytubefix import YouTube

from pyutube.utils import asking_video_or_audio, console, error_console
from pyutube.services.AudioService import AudioService
from pyutube.services.VideoService import VideoService
from pyutube.services.FileService import FileService


class DownloadService:
    def __init__(self, url: str, path: str, quality: str = '720p', is_audio: bool = False):
        self.url = url
        self.path = path
        self.quality = quality
        self.is_audio = is_audio

        self.video_service = VideoService(self.url, self.quality, self.path)
        self.audio_service = AudioService(url)
        self.file_service = FileService(self.path)

    def download(self) -> bool:
        video = self.video_service.search_process()
        self.video_service._print_video_info(video)
        video_id = video.video_id
        video_file, video_audio = self.video_service.get_selected_stream(video)

        if self.is_audio:
            self.download_audio(video_audio, video_id)
        else:
            self.download_video(video, video_id, video_file, video_audio)

        return True

    def download_audio(self, video_audio: YouTube, video_id: str) -> bool:
        audio_filename = self.file_service.generate_filename(video_audio, video_id, is_audio=True)

        audio_filename = os.path.join(self.path, audio_filename)
        audio_filename = self.file_service.handle_existing_file(audio_filename)

        try:
            if self.is_audio:
                console.print(
                    f"⏳ Downloading the audio...", style="info")

            self.file_service.save_file(video_audio, audio_filename)

        except Exception as error:
            error_console.print(
                f"❗ Error (please report this in github issue: https://github.com/Hetari/pyutube/issues):\n {error}")
            sys.exit()

        if self.is_audio:
            console.print("\n\n✅ Download completed", style="info")
        return True

    def download_video(self, video: YouTube, video_id: str, video_file: YouTube, video_audio: YouTube) -> bool:
        # Generate filename with title, quality, and file extension
        video_filename = self.file_service.generate_filename(video, video_id)
        video_filename = os.path.join(self.path, video_filename)
        video_filename = self.file_service.handle_existing_file(video_filename)

        try:
            console.print(
                f"⏳ Downloading the video...", style="info")
            self.file_service.save_file(video, video_filename)

        except Exception as error:
            error_console.print(
                f"❗ Error (please report this in github issue: https://github.com/Hetari/pyutube/issues):\n {error}")
            sys.exit()

        console.print("\n\n✅ Download completed", style="info")
        return self.quality

    def handle_video_or_audio(self):
        try:
            self.is_audio = asking_video_or_audio()
        except TypeError:
            return
        self.download()

    def get_playlist_links(self):
        handler = PlaylistHandler(self.url, self.path)
        handler.process_playlist()
