import click
from pytube import YouTube, Playlist
from pathlib import Path

from .config import PROGRESS_BAR_WIDTH
from .infos import show_infos
from .util import exiting


def progress_bar(chunk, file_handle, bytes_remaining):
    """Displays a progress bar during download"""
    current = (filesize - bytes_remaining) / filesize
    percent = int(("{0:.0f}").format(current * 100))

    progress = int(PROGRESS_BAR_WIDTH * current)
    bar = ("█" * progress) + ("-" * (PROGRESS_BAR_WIDTH - progress))

    if percent < 33:
        percent_str = click.style(f"{percent}%", fg="red")
    elif percent < 66:
        percent_str = click.style(f"{percent}%", fg="yellow")
    else:
        percent_str = click.style(f"{percent}%", fg="green")

    print(
        f"|{bar}| {percent_str}",
        end="\r",
        flush=True,
    )


def downloader(url: str, output_path: str, is_playlist: bool = False):
    """
    Download a video from YouTube specified by the `url` and saves it to the `output_path`

    Parameters:
        - url (str): The URL of the video or playlist to download.
        - output_path (str): The path where the downloaded video(s) will be saved
        - is_playlist (bool, optional): A boolean value indicating whether the `url` represents a playlist. Default is False

    Raises:
        - click.BadParameter: If the video is not found
    """
    global filesize
    yt = YouTube(url, on_progress_callback=progress_bar)

    show_infos(yt, is_playlist)

    video = yt.streams.get_highest_resolution()
    if not video:
        raise click.BadParameter("Video not found")
    filesize = video.filesize
    video.download(output_path)


def video_downloader(url: str, output_path: str):
    """
    Download a video from YouTube using the `downloader` function and handle exceptions

    Parameters:
        - url (str): The URL of the video to download
        - output_path (str): The path where the downloaded video will be saved
    """
    click.clear()
    try:
        downloader(url, output_path, False)
        click.echo()
        click.echo()
        click.echo()
        click.secho("Video downloaded successfully", fg="green", bold=True)
        click.secho("Saved in", fg="green")
        click.echo(output_path)
    except KeyboardInterrupt:
        exiting()
    except Exception as e:
        click.clear()
        click.secho(e, bold=True, fg="red", err=True)


def playlist_downloader(playlist: Playlist, output_path: str):
    """
    Download all videos from a YouTube playlist using the `downloader` function and handle exceptions

    Parameters:
        - playlist (Playlist): An instance of the `Playlist` class representing the playlist to download
        - output_path (str): The path where the downloaded videos will be saved
    """
    click.clear()
    click.secho(f"{playlist.title} | {playlist.owner}", fg="green", bold=True)
    click.secho(f"{playlist.length} Videos")
    click.secho(f"{f'{playlist.views:,}'.replace(',', '.')} Views")
    click.echo()

    for url in playlist.video_urls:
        try:
            downloader(url, output_path, True)
            click.echo()
            click.echo()
        except KeyboardInterrupt:
            exiting()
        except Exception as e:
            click.secho(e, bold=True, fg="red", err=True)

    click.echo()
    click.secho("Playlist downloaded successfully", fg="green", bold=True)
    click.secho("Saved in", fg="green")
    click.echo(output_path)


def path_manager(is_playlist: bool = False, playlist_title: str = "standard") -> str:
    """
    Manage the path where videos or playlists will be saved

    Parameters:
        - is_playlist (bool, optional): A boolean value indicating whether the content being downloaded is a playlist. Default is False
            If True, the function will create a folder named "playlists" to save playlist files
            If False, it will save videos in a folder named "videos"
        - playlist_title (str, optional): The title of the playlist being downloaded. This parameter is used if `is_playlist` is True. Default is "standard"

    Returns:
        - str: The path where the videos or playlists will be saved
    """
    current_path = Path.cwd()
    if is_playlist:
        folder_path = current_path / "playlists" / playlist_title
    else:
        folder_path = current_path / "videos"

    str_folder_path = str(folder_path)
    return str_folder_path


def download_manager(url: str):
    """
    Manage the download process for a single video or playlist from YouTube

    Parameters:
        - url (str): The URL of the video or playlist to download
    """
    if "playlist" in url:
        try:
            playlist = Playlist(url)
            if not playlist:
                raise click.BadParameter("Playlist not found")

            output_path = path_manager(True, playlist.title)
            playlist_downloader(playlist, output_path)
        except click.BadParameter as e:
            click.clear()
            click.secho(e, bold=True, fg="red", err=True)
    else:
        output_path = path_manager()
        video_downloader(url, output_path)
