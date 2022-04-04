# Twitter API
Using the public Twitter API to get access to Twitter data without requiring credentials for the Developer API. Implements the facade and dapter design patterns. Use responsibly. 

### Features
Currently under active development, however here are some things that you can do

- **Get user bio and their tweets (7200 max)**
- **Search using the live, top and users tabs**
- **Get tweet information from tweet id**
- [soon] Get explore page data
- [soon] Support pagination for all requests (only timeline is supported right now)
- [soon] View all tweet replies
- [soon] CLI tools
- [soon] Advanced search
- [soon] Testing 


## Installation 
Git clone this repo, cd into the root directory and run ```poetry install```. This does require [poetry](https://python-poetry.org/) to be installed on your local machine. 

## Usage
### - View Profiles
```python
from twitter.main import TwitterProfile

profile = TwitterProfile()

jack = profile.info('jack')
jack_timeline = profile.timeline('jack', count=200) # default count is 40

print(jack.description) 
# other profile attributes: username, id, rest_id, created_at, url, followers_count, following_count, banner_url, logo_url 

for tweet in espn_timeline:
    print(tweet.text) 
    # other tweet attributes: id, username, name, date, reply_count, retweet_count, like_count

```
### - Search
```python
from twitter.main import TwitterSearch

search = TwitterSearch()

premierleague_search = search.live("#premierleague")
worldcup_search = search.top("World Cup 2022 draw results")
elon_search = search.users("Elon Musk")

for tweet in premierleague_search:
    print(tweet.text) 
    # all tweet attributes are listed in the first example

for profile in ukraine_users:
    print(profile.username) 
    # all profile attributes are listed in the first example

```
### - View Tweet
```python
from twitter.main import TwitterTweet

tweet = TwitterTweet()

random_tweet = tweet.id(1509960093810442250)
print(random_tweet.text)
# all tweet attributes are listed in the first example

```

Main focus for the roadmap: CLI tools and paginated responses!

Use responsibly.
