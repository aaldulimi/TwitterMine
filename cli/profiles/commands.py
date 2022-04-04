import click
from twitter.main import TwitterProfile
import rich, rich.table, rich.box

@click.group('profile')
def cli():
    pass

@click.command()
@click.argument('username')
def info(username):
    profile = TwitterProfile()
    result = profile.info(username)
    
    table = rich.table.Table(box=rich.box.SQUARE, show_footer=True)
    table.add_column(f'[cyan]@{result.username} [white]{result.name}', '[cyan]{} Following     {} Followers \t [yellow]{}'.format(result.following_count, result.followers_count, result.url), width=75)
    table.add_row(result.description)
        
    rich.print(table)


@click.command()
@click.argument('username')
@click.option('--count', default=40, show_default=True)
def timeline(username, count):
    profile = TwitterProfile()
    result = profile.timeline(username, count)
    
    for tweet in result:
        table = rich.table.Table(box=rich.box.SQUARE, show_footer=True)
        table.add_column(f"[cyan]@{tweet.username}[/] [white]{tweet.name}[/] [yellow]{tweet.date}", "[cyan]likes: [white]{:<15}[/] retweets: [white]{:<15}[/] replies: [white]{:<15}[/]".format(tweet.like_count, tweet.retweet_count, tweet.reply_count), justify="left", no_wrap=False, width=75)
        table.add_row(tweet.text)

        rich.print(table)



cli.add_command(info)
cli.add_command(timeline)

if __name__ == "__main__":
    cli()