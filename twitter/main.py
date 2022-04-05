import dataclasses
import typing 
import datetime 
import os
import random
import requests 
import time 
import datetime
import functools
import json
import urllib.parse


@dataclasses.dataclass
class User:
    """A very minimal user dataclass that only contains information usually displayed by the profile banner of a user."""

    username: typing.Optional[str] = None
    id: typing.Optional[int] = None
    rest_id: typing.Optional[int] = None
    name: typing.Optional[str] = None
    created_at: typing.Optional[datetime.datetime] = None
    description: typing.Optional[str] = None
    url: typing.Optional[str] = None
    followers_count: typing.Optional[int] = None
    following_count: typing.Optional[int] = None
    banner_url: typing.Optional[str] = None
    logo_url: typing.Optional[str] = None


@dataclasses.dataclass
class Tweet:
    """A very minimal tweet dataclass that only contains information usually displayed by a single tweet."""

    id: typing.Optional[int] = None
    username: typing.Optional[str] = None
    name: typing.Optional[str] = None
    date: typing.Optional[datetime.datetime] = None
    text: typing.Optional[str] = None
    reply_count: typing.Optional[int] = None
    retweet_count: typing.Optional[int] = None
    like_count: typing.Optional[int] = None
    
    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.date)



class Config():  
    """Contains the auth token and guest token in order to send authorised requests to the API"""

    AUTH_BEARER = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

    def __init__(self):
        self._headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.{random.randint(0, 9999)} Safari/537.{random.randint(0, 99)}',    
            'Accept-Language': 'en-US,en;q=0.5',
            'content-type': "application/json",
            'Authorization': Config.AUTH_BEARER
            }

    def _get_guest_token(self):
        guest_response = requests.post('https://api.twitter.com/1.1/guest/activate.json', headers=self._headers)
        guest_token = guest_response.json()['guest_token']

        return guest_token

    def _deep_get(data, keys, default=None):
        return functools.reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), data)

    @property
    def guest_token(self):
        if os.environ.get("guest_token", None) is None:
            os.environ['guest_token'] = self._get_guest_token()

        return os.environ['guest_token']
    

class TwitterProfile():
    """Provides methods to get basic user profile information and their timeline."""

    def __init__(self):
        self.config = Config()
        self.headers = self.config._headers
        self.headers['x-guest-token'] = f'{self.config.guest_token}'

    def _json_to_tweet(self, tweet, username, name):
        tweet_id = int(tweet['sortIndex'])
        tweet_text = tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
        tweet_likes = tweet['content']['itemContent']['tweet_results']['result']['legacy']['favorite_count']
        tweet_retweets = tweet['content']['itemContent']['tweet_results']['result']['legacy']['retweet_count']
        tweet_replies = tweet['content']['itemContent']['tweet_results']['result']['legacy']['reply_count']

        date = tweet['content']['itemContent']['tweet_results']['result']['legacy']['created_at']
        date = time.strptime(date, '%a %b %d %H:%M:%S %z %Y')     
        date = datetime.datetime.fromtimestamp(time.mktime(date))
        
        tweet_obj = Tweet(
            id = tweet_id,
            username =  username,
            name = name,
            date = date,
            text = tweet_text,
            reply_count = tweet_replies,      
            retweet_count = tweet_retweets,
            like_count = tweet_likes
        )

        return tweet_obj

    def info(self, username):
        self.headers['referer'] = f'https://twitter.com/{username}' # how to reference attributes of classmethod within other methods

        url = 'https://api.twitter.com/graphql/-xfUfZsnR_zqjFd-IfrN5A/UserByScreenName'
        params = {'variables': json.dumps({'screen_name': username, 'withHighlightedLabel': True}, separators = (',', ':'))}
        params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()

        id = data['data']['user']['id']
        rest_id = data['data']['user']['rest_id']
        name = data['data']['user']['legacy']['name']
        username = data['data']['user']['legacy']['screen_name']

        date = data['data']['user']['legacy']['created_at']
        date = time.strptime(date, '%a %b %d %H:%M:%S %z %Y')     
        date = datetime.datetime.fromtimestamp(time.mktime(date))
        
        description = data['data']['user']['legacy']['description']
        url = data.get("data", {}).get('user', {}).get('legacy', {}).get('url', None)
        followers_count = data['data']['user']['legacy']['followers_count']
        following_count = data['data']['user']['legacy']['friends_count']
        banner_url = data.get('data', {}).get('user', {}).get('legacy', {}).get('profile_banner_url', None) 
        logo_url = data.get("data", {}).get('user', {}).get('legacy', {}).get('profile_image_url_https', None) 
        
        return User(
            id = id,
            rest_id = rest_id, 
            name = name,
            username = username,
            created_at = date,
            description = description,
            url = url,
            followers_count = followers_count,
            following_count = following_count,
            banner_url = banner_url,
            logo_url = logo_url
        )

    def timeline(self, username, count=40):
        self.headers['referer'] = f'https://twitter.com/{username}' # how to reference attributes of classmethod within other methods

        profile = self.info(username)
        user_id = profile.rest_id

        url = f'https://mobile.twitter.com/i/api/graphql/y3KhIGmsE79hC1zGtPdAOQ/UserTweets'

        if count < 7: adjusted_count = 7
        else: adjusted_count = count

        params_dict = {
            "userId": user_id,
            "count": adjusted_count,
            "includePromotedContent":True,
            "withQuickPromoteEligibilityTweetFields":True,
            "withSuperFollowsUserFields":True,
            "withDownvotePerspective":False,
            "withReactionsMetadata":False,
            "withReactionsPerspective":False,
            "withSuperFollowsTweetFields":True,
            "withVoice":True,
            "withV2Timeline":False,
            "__fs_dont_mention_me_view_api_enabled":False,
            "__fs_interactive_text_enabled":False,
            "__fs_responsive_web_uc_gql_enabled":False
        }

        params_variables = json.dumps(params_dict, separators = (',', ':'))
        params = {'variables': params_variables}
        params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

        tweet_collection = Collection()
        total = 0
        instructions = 1

        while (total < count):
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()

            tweet_entries = data['data']['user']['result']['timeline']['timeline']['instructions'][instructions]['entries']
            for tweet in tweet_entries:

                tweet_module = tweet['content']['entryType']

                if tweet_module == 'TimelineTimelineCursor':
                    if tweet['content']['cursorType'] == 'Bottom':
                        bottom_cursor = tweet['content']['value']
                        

                if tweet_module == 'TimelineTimelineItem':
                    tweet_obj = self._json_to_tweet(tweet, username, profile.name)
                    tweet_collection.add_tweet(tweet_obj)
                    total += 1

                    if total >= count: break

            
            if total >= count: break
            params_dict['cursor'] = bottom_cursor
            params_variables = json.dumps(params_dict, separators = (',', ':'))
            params = {'variables': params_variables}
            params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
            instructions = 0

        return tweet_collection.tweets


class TwitterSearch():
    """Provides methods to get hashtag, timeline and search data. automatically shows top, can filter to latest and show profiles."""

    def __init__(self):
        self._config = Config()
        self._headers = self._config._headers
        self._headers['x-guest-token'] = f'{self._config.guest_token}'
        self._params = {
            'include_profile_interstitial_type': 1,
            'include_blocking': 1,
            'include_blocked_by': 1,
            'include_followed_by': 1,
            'include_want_retweets': 1,
            'include_mute_edge': 1,
            'include_can_dm': 1,
            'include_can_media_tag': 1,
            'include_ext_has_nft_avatar': 1,
            'skip_status': 1,
            'cards_platform': 'Web-12',
            'include_cards': 1,
            'include_ext_alt_text': True,
            'include_quote_count': True,
            'include_reply_count': 1,
            'tweet_mode': 'extended',
            'include_entities': True,
            'include_user_entities': True,
            'include_ext_media_color': True,
            'include_ext_media_availability': True,
            'include_ext_sensitive_media_warning': True,
            'include_ext_trusted_friends_metadata': True,
            'send_error_codes': True,
            'simple_quoted_tweet': True,
            'count': 40,
            'query_source': 'typed_query',
            'pc': 1,
            'spelling_corrections': 1,
            'ext': 'mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,enrichments,superFollowMetadata'
        }

        self._url = 'https://twitter.com/i/api/2/search/adaptive.json'


    def _json_to_tweets(self, data: dict = None):
        if data is None:
            raise ValueError("No json data provided.")
        
        tweet_collection = Collection()

        for tweet_id in data['globalObjects']['tweets']:
            tweet_text = data['globalObjects']['tweets'][tweet_id]['full_text']
            tweet_likes = data['globalObjects']['tweets'][tweet_id]['favorite_count']
            tweet_retweets = data['globalObjects']['tweets'][tweet_id]['retweet_count']
            tweet_replies = data['globalObjects']['tweets'][tweet_id]['reply_count']

            date = data['globalObjects']['tweets'][tweet_id]['created_at']
            date = time.strptime(date, '%a %b %d %H:%M:%S %z %Y')     
            date = datetime.datetime.fromtimestamp(time.mktime(date))

            user_id = str(data['globalObjects']['tweets'][tweet_id]['user_id'])
            username = data['globalObjects']['users'][user_id]['screen_name']
            name = data['globalObjects']['users'][user_id]['name']

            tweet_obj = Tweet(
                id = tweet_id,
                username =  username,
                name = name,
                date = date,
                text = tweet_text,
                reply_count = tweet_replies,      
                retweet_count = tweet_retweets,
                like_count = tweet_likes
            )

            tweet_collection.add_tweet(tweet_obj)

        return tweet_collection
    
    def _json_to_profiles(self, data: dict = None):
        if data is None:
            raise ValueError("No json data provided.")

        profile_collection = Collection()

        for user_id in data:
            id = data[user_id]['id']
            rest_id = data[user_id]['id']
            name = data[user_id]['name']
            username = data[user_id]['screen_name']

            date = data[user_id]['created_at'] 
            date = time.strptime(date, '%a %b %d %H:%M:%S %z %Y')     
            date = datetime.datetime.fromtimestamp(time.mktime(date))

            description = data[user_id]['description']
            url = data[user_id]['url']
            followers_count = data[user_id]['followers_count']
            following_count = data[user_id]['friends_count']

            banner_url = data[user_id].get('profile_banner_url', '')
            logo_url = data[user_id].get('profile_image_url_https', '')

            profile = User(
                id=id,
                rest_id=rest_id,
                name = name,
                username = username,
                created_at = date,
                description = description,
                url = url,
                followers_count = followers_count,
                following_count = following_count,
                banner_url = banner_url,
                logo_url = logo_url,
            )

            profile_collection.add_profile(profile)

        return profile_collection

    def top(self, query):
        self._headers['referer'] = f'https://twitter.com/search?q=%{query}&src=typed_query&f=live'
        self._params['q'] = f'{query}' 

        response = requests.get(self._url, headers=self._headers, params=self._params)
        data = response.json()

        del self._params['q']

        collection = self._json_to_tweets(data)
        return collection.tweets

        
    def live(self, query):
        self._headers['referer'] = f'https://twitter.com/search?q=%{query}&src=typed_query&f=live'
        self._params['q'] = f'{query}'
        self._params['tweet_search_mode'] = 'live' 

        response = requests.get(self._url, headers=self._headers, params=self._params)
        data = response.json()

        del self._params['q']
        del self._params['tweet_search_mode']

        collection = self._json_to_tweets(data)
    
        return collection.tweets
        
    def users(self, query):
        self._headers['referer'] = f'https://twitter.com/search?q=%{query}&src=typed_query&f=live'
        self._params['q'] = f'{query}' 
        self._params['result_filter'] = 'user'
        self._params['tweet_search_mode'] = 'live'

        response = requests.get(self._url, headers=self._headers, params=self._params)
        data = response.json()
        data = data['globalObjects']['users']

        del self._params['q']
        del self._params['result_filter']
        del self._params['tweet_search_mode']

        collection = self._json_to_profiles(data)

        return collection.profiles


class TwitterTweet():
    def __init__(self) -> None:
        self._config = Config()
        self._headers = self._config._headers
        self._headers['x-guest-token'] = f'{self._config.guest_token}'

        self._params = {
            "with_rux_injections":False,
            "includePromotedContent":True,
            "withCommunity":True,
            "withQuickPromoteEligibilityTweetFields":True,
            "withBirdwatchNotes":False,
            "withSuperFollowsUserFields":True,
            "withDownvotePerspective":False,
            "withReactionsMetadata":False,
            "withReactionsPerspective":False,
            "withSuperFollowsTweetFields":True,
            "withVoice":True,
            "withV2Timeline":False,
            "__fs_dont_mention_me_view_api_enabled":False,
            "__fs_interactive_text_enabled":True,
            "__fs_responsive_web_uc_gql_enabled":False
        }

    def _json_to_tweet(self, data):
        data = data['data']['threaded_conversation_with_injections']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']
        
        tweet_id = int(data['legacy']['conversation_id_str'])

        tweet_text = data['legacy']['full_text']
        tweet_likes = data['legacy']['favorite_count']
        tweet_retweets = data['legacy']['retweet_count']
        tweet_replies = data['legacy']['reply_count']

        date = data['legacy']['created_at']
        date = time.strptime(date, '%a %b %d %H:%M:%S %z %Y')     
        date = datetime.datetime.fromtimestamp(time.mktime(date))

        user_id = data['core']['user_results']['result']['rest_id']
        username = data['core']['user_results']['result']['legacy']['screen_name']
        name = data['core']['user_results']['result']['legacy']['name']

        tweet = Tweet(
                id = tweet_id,
                username =  username,
                name = name,
                date = date,
                text = tweet_text,
                reply_count = tweet_replies,      
                retweet_count = tweet_retweets,
                like_count = tweet_likes
            )
        
        return tweet

    def id(self, id):
        self._headers['referer'] = f'https://twitter.com/ESPNFC/status/{id}'
        self._params['focalTweetId'] = f'{id}'
        
        url = 'https://twitter.com/i/api/graphql/LJ_TjoWGgNTXCl7gfx4Njw/TweetDetail'
        params = json.dumps(self._params)
        params = {'variables': params}
        params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

        response = requests.get(url, headers=self._headers, params=params)
        data = response.json()

        tweet = self._json_to_tweet(data)

        return tweet
        


class Collection():
    """A list of tweets or users of the Tweet or User class from a timeline, hashtag or a search page."""

    def __init__(self, tweets: typing.List = list(), profiles: typing.List = list()):
        self.tweets = tweets
        self.profiles = profiles
        
    def add_tweet(self, tweet: Tweet) -> None:
        if tweet not in self.tweets:
            self.tweets.append(tweet)
        return
    
    def add_profile(self, profile: User) -> None:
        if profile not in self.profiles:
            self.profiles.append(profile)
        return
        


if __name__ == "__main__":
    pass
