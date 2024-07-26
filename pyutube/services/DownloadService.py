import os
import sys
import threading

from pyutube.utils import console, error_console, asking_video_or_audio, ask_playlist_video_names
from pyutube.downloader import download
from pyutube.handlers.PlaylistHandler import PlaylistHandler


class DownloadService:
    def __init__(self, url, path):
        self.url = url
        self.path = path

    def download_audio(self):
        download(self.url, self.path, is_audio=True)

    def download_video(self):
        download(self.url, self.path, is_audio=False)

    def handle_video_or_audio(self):
        # ask if the user wants to download audio, or video?
        try:
            is_audio = asking_video_or_audio()
        except TypeError:
            return
        download(self.url, self.path, is_audio)

    def handle_playlist(self):
        handler = PlaylistHandler(self.url, self.path)
        handler.process_playlist()
