import click
from pytube import YouTube

from .infos import show_infos


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
        yt = YouTube(url)

        click.clear()
        show_infos(yt)

        video = yt.streams.get_highest_resolution()
        if not video:
            raise click.BadParameter("Video not found")

        video.download(output_path)

    except Exception as e:
        click.clear()
        click.pause(click.style("Video not found", bold=True, fg="red"), err=True)
