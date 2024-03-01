import click
import validators

from .downloader import downloader


def exiting():
    click.clear()
    click.secho("Aborting", bold=True, fg="green")
    exit()


def is_valid_url(url: str):
    if not isinstance(url, str):
        raise click.BadParameter(f"The url must be a string")
    elif not validators.url(url):
        raise click.BadParameter("Invalid URL")
    elif not "youtube.com" in url:
        raise click.BadParameter("The URL must be from YouTube")

    return url


def main():
    output_path = "./videos/"

    while True:
        click.clear()
        try:
            url = click.prompt("Please enter an url")
            if is_valid_url(url):
                break
        except click.BadParameter as e:
            click.pause(click.style(e, bold=True, fg="red"), err=True)
        except click.exceptions.Abort:
            exiting()

    downloader(url, output_path)
