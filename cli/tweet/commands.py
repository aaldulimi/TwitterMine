import click
from twitter.main import TwitterTweet
import rich, rich.table, rich.box


@click.command('tweet')
@click.argument('id')
def cli(id):
    twitter = TwitterTweet()
    tweet = twitter.id(id)
    
    table = rich.table.Table(box=rich.box.SQUARE, show_footer=True)
    table.add_column(f"[cyan]@{tweet.username}[/] [white]{tweet.name}[/] [yellow]{tweet.date}", "[cyan]likes: [white]{:<15}[/] retweets: [white]{:<15}[/] replies: [white]{:<15}[/]".format(tweet.like_count, tweet.retweet_count, tweet.reply_count), justify="left", no_wrap=False, width=75)
    table.add_row(tweet.text)

    rich.print(table)


if __name__ == "__main__":
    cli()
