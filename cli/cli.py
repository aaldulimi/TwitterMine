import click
from search import commands as search
from profiles import commands as profile
from tweet import commands as tweet


@click.group()
def entry_point():
    pass

entry_point.add_command(search.cli)
entry_point.add_command(profile.cli)
entry_point.add_command(tweet.cli)


if __name__ == "__main__":
    entry_point()
