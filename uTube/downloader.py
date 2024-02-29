# Logic for downloading YouTube videos
import time
import pytube
from pytube import YouTube
from rich.progress import track


def download_vide(url):
    for _ in track(range(20), description="Processing..."):
        time.sleep(1)
