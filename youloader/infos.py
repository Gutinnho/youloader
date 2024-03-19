import click
from datetime import datetime as Datetime
from pytube import YouTube

from .config import MAX_TITLE_LENGTH


def format_time(time: int) -> str:
    """
    Formats an integer value representing seconds into a string in the format hours:minutes:seconds

    Parameters:
    - time (int): An integer representing the number of seconds to be formatted

    Returns:
    - str: A formatted string representing the time in the format "hours:minutes:seconds" or "minutes:seconds" if the time is less than an hour
    """
    assert time > 0, "time must be a positive integer"

    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60

    if hours == 0:
        return f"{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_date(date: Datetime) -> str:
    """
    Formats a datetime object into a string in the "dd/mm/yyyy" format

    Parameters:
    - date (datetime): A datetime object representing the date to be formatted

    Returns:
    - str: A formatted string representing the date in the "dd/mm/yyyy" format
    """
    date_formated = date.strftime("%d/%m/%Y")

    return date_formated


def show_infos(stream: YouTube, is_playlist: bool):
    """
    Show the information of a video

    Parameters:
        - stream (YouTube): An instance of the `YouTube` class representing the video to display information about
        - is_playlist (bool): A boolean value to indicate whether it is a playlist, changing the way information is displayed

    This function prints the following information about the video:
        - Title: The title of the video, truncated to 50 characters if it exceeds this length
        - Author: The author of the video
        - Duration: The duration of the video in hours, minutes, and seconds format
        - Published Date: The date when the video was published in the format "dd/mm/yyyy"
        - Views: The number of views the video has, formatted with thousand separators
    """

    title = (
        stream.title[:MAX_TITLE_LENGTH] + "..."
        if len(stream.title) > MAX_TITLE_LENGTH
        else stream.title
    )
    author = stream.author
    time = format_time(stream.length)
    publish_date = stream.publish_date
    if publish_date:
        published_at = format_date(publish_date)
    views = f"{stream.views:,}".replace(",", ".")

    (
        click.echo(f"{title} | {author}")
        if is_playlist
        else click.echo(f"{title} \n{author}")
    )
    if publish_date:
        click.echo(f"{time} | {published_at}")
    else:
        click.echo(f"{time}")
    click.echo(f"{views} Views")

    click.echo()
