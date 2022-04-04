import click
from twitter.main import TwitterSearch
import rich, rich.table, rich.box

@click.group('search')
def cli():
    pass

@click.command()
@click.argument('query')
def live(query):
    search = TwitterSearch()
    result = search.live(query)
    
    for tweet in result:
        table = rich.table.Table(box=rich.box.SQUARE, show_footer=True)
        table.add_column(f"[cyan]@{tweet.username}[/] [white]{tweet.name}[/] [yellow]{tweet.date}", "[cyan]likes: [white]{:<15}[/] retweets: [white]{:<15}[/] replies: [white]{:<15}[/]".format(tweet.like_count, tweet.retweet_count, tweet.reply_count), justify="left", no_wrap=False, width=75)
        table.add_row(tweet.text)

        rich.print(table)


@click.command()
@click.argument('query')
def top(query):
    search = TwitterSearch()
    result = search.top(query)
    
    for tweet in result:
        table = rich.table.Table(box=rich.box.SQUARE, show_footer=True)
        table.add_column(f"[cyan]@{tweet.username}[/] [white]{tweet.name}[/] [yellow]{tweet.date}", "[cyan]likes: [white]{:<15}[/] retweets: [white]{:<15}[/] replies: [white]{:<15}[/]".format(tweet.like_count, tweet.retweet_count, tweet.reply_count), justify="left", no_wrap=False, width=75)
        table.add_row(tweet.text)

        rich.print(table)


@click.command()
@click.argument('query')
def users(query):
    search = TwitterSearch()
    result = search.users(query)
    
    for profile in result:
        table = rich.table.Table(box=rich.box.SQUARE, show_footer=True)
        table.add_column(f'[cyan]@{profile.username} [white]{profile.name}', '[cyan]{} Following     {} Followers \t [yellow]{}'.format(profile.following_count, profile.followers_count, profile.url), width=75)
        table.add_row(profile.description)
        
        rich.print(table)



cli.add_command(live)
cli.add_command(top)
cli.add_command(users)

if __name__ == "__main__":
    cli()
