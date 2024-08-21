import os
import sys
import threading

from pytubefix.helpers import safe_filename
from pytubefix import Playlist

from pyutube.utils import console, asking_video_or_audio, ask_playlist_video_names


class PlaylistHandler:
    playlist_videos = []

    def __init__(self, url: str, path: str):
        self.url: str = url
        self.path: str = path

    def process_playlist(self):
        """
        Process the playlist by asking for the audio or video, downloading the playlist,
        then asking for which video to download and downloading it.
        """
        try:
            is_audio = asking_video_or_audio()
        except TypeError:
            # If the user cancelled, return
            return

        playlist_stream = Playlist(self.url)

        p_title = playlist_stream.title
        p_total = playlist_stream.length
        p_videos = playlist_stream.videos

        self.get_all_playlist_videos_title(p_videos)

        new_path = self.check_for_downloaded_videos(p_title, p_total)

        console.print("Chose what video you want to download")
        videos_selected = ask_playlist_video_names(self.playlist_videos)

        return new_path, is_audio, videos_selected

    def fetch_title_thread(self, video):
        video_title = safe_filename(video.title)
        video_id = video.video_id
        self.playlist_videos.append((video_title, video_id))

    def get_all_playlist_videos_title(self, videos):
        # Use threading to fetch titles concurrently
        title_threads = []

        # Create and start a thread for each video
        for video in videos:
            thread = threading.Thread(
                target=self.fetch_title_thread, args=(video,))
            thread.start()
            title_threads.append(thread)

        # Wait for all threads to finish
        for thread in title_threads:
            thread.join()

    @staticmethod
    def show_playlist_info(title, total):
        console.print(f"\nPlaylist title: {title}\n", style="info")
        console.print(f"Total videos: {total}\n", style="info")

    def create_playlist_folder(self, title):
        os.makedirs(title, exist_ok=True)
        return os.path.join(self.path, title)

    def check_for_downloaded_videos(self, title, total):
        new_path = self.create_playlist_folder(title)

        # check if there is any video already downloaded in the past
        for file in os.listdir(new_path):
            for video in self.playlist_videos:
                if file.startswith(video):
                    self.playlist_videos.remove(video)
                    # Exit the inner loop since we found a match
                    break

        if not self.playlist_videos:
            console.print(f"All playlist are already downloaded in this directory, see '{title}' folder", style="info")
            sys.exit()

        self.show_playlist_info(title, total)
        return new_path
