import os
import sys
from pyutube.downloader import download
from pyutube.utils import console, error_console, asking_video_or_audio, ask_playlist_video_names
from pytubefix.helpers import safe_filename
import threading


class PlaylistHandler:
    playlist_videos = []

    def __init__(self, url, path):
        self.url = url
        self.path = path

    def process_playlist(self):
        try:
            is_audio = asking_video_or_audio()
            print(is_audio)
        except TypeError:
            return
        playlist = download(self.url, self.path, is_audio, is_playlist=True)

        # links = playlist.video_urls
        title = playlist.title
        total = playlist.length
        videos = playlist.videos

        # Use threading to fetch titles concurrently
        title_threads = self.handle_playlist_videos(videos)

        # Now all video titles are stored in the video_titles list
        console.print(f"\nPlaylist title: {title}\n", style="info")
        console.print(f"Total videos: {total}\n", style="info")

        os.makedirs(title, exist_ok=True)
        new_path = os.path.join(self.path, title)

        # check if there is any video already downloaded in the past
        for file in os.listdir(new_path):
            for video in self.playlist_videos:
                if file.startswith(video):
                    self.playlist_videos.remove(video)
                    # Exit the inner loop since we found a match
                    break

        if not self.playlist_videos:
            console.print(f"All playlist are already downloaded in this directory, see '{
                title}' folder", style="info")
            sys.exit()

        console.print("Chose what video you want to download")
        videos_selected = ask_playlist_video_names(self.playlist_videos)

        for index, video_id in enumerate(videos_selected):
            url = f"https://www.youtube.com/watch?v={video_id}"

            if index == 0:
                quality = download(url, new_path, is_audio, is_playlist=False)
                continue
            download(url, new_path, is_audio,
                     quality_choice=quality,
                     is_playlist=False)

    def fetch_title_thread(self, video):
        video_title = safe_filename(video.title)
        video_id = video.video_id
        self.playlist_videos.append((video_title, video_id))

    def handle_playlist_videos(self, videos):
        # sourcery skip: inline-immediately-returned-variable, move-assign-in-block
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

        return title_threads
