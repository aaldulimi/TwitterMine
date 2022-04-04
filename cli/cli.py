import click
from .search import commands as search
from .profiles import commands as profile
from .tweet import commands as tweet


@click.group()
def cli():
    pass

cli.add_command(search.cli)
cli.add_command(profile.cli)
cli.add_command(tweet.cli)


def main():
    cli()
