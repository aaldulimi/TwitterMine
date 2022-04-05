# Twitter API
Using the public Twitter API to get access to Twitter data without requiring credentials for the Developer API. Can be used as library, or from the CLI (refer to [Usage](#usage)). Implements the facade and dapter design patterns. Use responsibly. 

## Contents
- [Twitter API](#twitter-api)
  - [Contents](#contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [View Profiles](#view-profiles)
    - [Search](#search)
    - [View Tweet](#view-tweet)
    - [CLI](#cli)


   

## Features
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
- [soon] Support images (ASCII)


## Installation 
Git clone this repo, cd into the root directory and run ```poetry install```. This does require [poetry](https://python-poetry.org/) to be installed on your local machine. 

## Usage
### View Profiles
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
### Search
```python
from twitter.main import TwitterSearch

search = TwitterSearch()

premierleague_search = search.live("#premierleague")
worldcup_search = search.top("World Cup 2022 draw results")
elon_search = search.users("Elon Musk")

for tweet in premierleague_search:
    print(tweet.text) 
    # all tweet attributes are listed in the first example

for profile in elon_search:
    print(profile.username) 
    # all profile attributes are listed in the first example

```
### View Tweet
```python
from twitter.main import TwitterTweet

tweet = TwitterTweet()

random_tweet = tweet.id(1509960093810442250)
print(random_tweet.text)
# all tweet attributes are listed in the first example

```

### CLI
After you run `poetry install`, accessing the cli tools is done by typing `twitter --help`. Although you should refer to the `--help` page for the full documentation, here is a sample of what you can do:
```
poetry run twitter profile info "jack"
poetry run twitter profile timeline "jack" --count 100
```
```
poetry run twitter search live "#premierleague"
poetry run twitter search users "Elon Musk"
```
```
poetry run twitter tweet 20 1509960093810442250
```


Use responsibly.
