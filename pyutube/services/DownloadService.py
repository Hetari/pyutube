from pyutube.handlers.PlaylistHandler import PlaylistHandler
import os
import sys

from pytubefix import YouTube

from pyutube.utils import asking_video_or_audio, console, error_console
from pyutube.services.AudioService import AudioService
from pyutube.services.VideoService import VideoService
from pyutube.services.FileService import FileService


class DownloadService:
    def __init__(self, url: str, path: str, quality: str, is_audio: bool = False):
        self.url = url
        self.path = path
        self.quality = quality
        self.is_audio = is_audio

        self.video_service = VideoService(self.url, self.quality, self.path)
        self.audio_service = AudioService(url)
        self.file_service = FileService()

    def download(self) -> bool:
        video, video_id,  streams, video_audio, self.quality = self.download_preparing()

        if self.is_audio:
            self.download_audio(video, video_audio, video_id)
        else:
            video_file = self.video_service.get_video_streams(self.quality, streams)
            if not video_file:
                error_console.print(
                    "Something went wrong while downloading the video.")
                raise RuntimeError("Failed to download the video stream.")

            return self.download_video(video, video_id, video_file, video_audio)

        return True

    def download_audio(self, video: YouTube, video_audio: YouTube, video_id: str) -> bool:
        audio_filename = self.file_service.generate_filename(video_audio, video_id, is_audio=True)

        audio_filename = os.path.join(self.path, audio_filename)
        audio_filename = self.file_service.handle_existing_file(
            video, video_id, audio_filename, self.path, self.is_audio)

        try:
            if self.is_audio:
                console.print("⏳ Downloading the audio...", style="info")

            self.file_service.save_file(video_audio, audio_filename,  self.path)

        except Exception as error:
            error_console.print(
                f"❗ Error (please report this in github issue: https://github.com/Hetari/pyutube/issues):\n {error}")
            sys.exit()

        if self.is_audio:
            console.print("\n\n✅ Download completed", style="info")
            return True
        return audio_filename

    def download_video(self, video: YouTube, video_id: str, video_file: YouTube, video_audio: YouTube) -> bool:
        # Generate filename with title, quality, and file extension
        video_filename = self.file_service.generate_filename(video_file, video_id,)
        video_filename = os.path.join(self.path, video_filename)
        video_filename = self.file_service.handle_existing_file(
            video, video_id, video_filename, self.path, self.is_audio)

        try:
            console.print("⏳ Downloading the video...", style="info")

            self.file_service.save_file(video_file, video_filename, self.path)
            audio_filename = self.download_audio(video, video_audio, video_id)

            self.video_service.merging(video_filename, audio_filename)

        except Exception as error:
            error_console.print(
                f"❗ Error (please report this in github issue: https://github.com/Hetari/pyutube/issues):\n {error}")
            sys.exit()

        console.print("\n\n✅ Download completed", style="info")
        return self.quality

    def asking_video_or_audio(self):
        try:
            self.is_audio = asking_video_or_audio()
        except TypeError:
            return
        self.download()

    def get_playlist_links(self):
        handler = PlaylistHandler(self.url, self.path)
        new_path, is_audio, videos_selected = handler.process_playlist()

        # Download the selected videos
        for index, video_id in enumerate(videos_selected):
            url = f"https://www.youtube.com/watch?v={video_id}"

            self.url = url
            self.path = new_path
            self.is_audio = is_audio

            if index == 0:
                # If it is the first video, download it and store the quality
                self.video_service = VideoService(self.url, self.quality, self.path)
                quality = self.download()
                continue

            # If it is not the first video, download it with the stored quality

            self.quality = quality
            self.video_service = VideoService(self.url, self.quality, self.path)
            self.download()

    def download_preparing(self):
        video = self.video_service.search_process()
        self.video_service._print_video_info(video)
        video_id = video.video_id
        streams, video_audio, self.quality = self.video_service.get_selected_stream(video, self.is_audio)

        return video, video_id,  streams, video_audio, self.quality
