# Twitter API
Using the public Twitter API to get access to Twitter data without requiring credentials for the Developer API. Can be used as library, or from the CLI (refer to [Usage](#usage)). Implements the facade and dapter design patterns. Use responsibly. 

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#third-example)

   3.1. [Profiles](#31-view-profiles)

   3.1.  [Search](#32-search)

   3.3.  [View Tweet](#33-view-tweet)

   3.4.  [CLI](#34-cli)

### Features
Currently under active development, however here are some things that you can do

- **Get user bio and their tweets (7200 max)**
- **Search using the live, top and users tabs**
- **Get tweet information from tweet id**
- **CLI tools**
- [soon] Get explore page data
- [soon] Support pagination for all requests (only timeline is supported right now)
- [soon] View all tweet replies
- [soon] Advanced search
- [soon] Testing 


## Installation 
Git clone this repo, cd into the root directory and run ```poetry install```. This does require [poetry](https://python-poetry.org/) to be installed on your local machine. 

## Usage
### - 3.1 View Profiles
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
### - 3.2 Search
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
### - 3.3 View Tweet
```python
from twitter.main import TwitterTweet

tweet = TwitterTweet()

random_tweet = tweet.id(1509960093810442250)
print(random_tweet.text)
# all tweet attributes are listed in the first example

```

### - 3.4 CLI
After you run `poetry install`, accessing the cli tools is done by typing `twitter --help`. Although you should refer to the `--help` page for the full documentation, here is a sample of what you can do:
```
twitter profile info "jack"
twitter profile timeline "jack" --count 100
```
```
twitter search live "#premierleague"
twitter search users "Elon Musk"
```
```
twitter tweet 20 1509960093810442250
```


Use responsibly.
