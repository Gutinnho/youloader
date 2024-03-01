import click
from pytube import YouTube

from .config import PROGRESS_BAR_WIDTH
from .infos import show_infos


def progress_bar(chunk, file_handle, bytes_remaining):
    """Displays a progress bar during download"""
    current = (filesize - bytes_remaining) / filesize
    percent = ("{0:.0f}").format(current * 100)

    progress = int(PROGRESS_BAR_WIDTH * current)
    bar = ("█" * progress) + ("-" * (PROGRESS_BAR_WIDTH - progress))

    print(
        f"|{bar}| {percent}%",
        end="\r",
        flush=True,
    )


def downloader(url: str, output_path: str) -> None:
    """
    Downloads a video from the specified URL to the specified output path

    Parameters:
    - url (str): The URL of the video to be downloaded
    - output_path (str): The path where the downloaded video will be saved

    Raises:
    - click.BadParameter: If the video is not found
    """
    try:
        global filesize

        yt = YouTube(url, on_progress_callback=progress_bar)

        click.clear()
        show_infos(yt)

        video = yt.streams.get_highest_resolution()
        if not video:
            raise click.BadParameter("Video not found")
        filesize = video.filesize

        video.download(output_path)

    except Exception as e:
        click.clear()
        click.pause(click.style("Video not found", bold=True, fg="red"), err=True)
