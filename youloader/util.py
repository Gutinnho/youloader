import click


def exiting():
    click.clear()
    click.secho("Aborting", bold=True, fg="green")
    exit()
