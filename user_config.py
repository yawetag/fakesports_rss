import praw
from dhooks import Webhook

# praw = Python Reddit API Wrapper
# go to https://www.reddit.com/prefs/apps
# finish this description

reddit = praw.Reddit(
    client_id     = '-- add something here --',
    client_secret = '-- add something here --',
    user_agent    = '-- add something here --'
)

# List of players who do *not* want to be pinged. This should be in the following format:
# ping_exclude = ['Stupido Einsteiny', 'Mark Schihne']
ping_exclude = []

# List of RSS feeds for each league. Delete those you don't need and modify those you do, while maintaining the formatting.
rss_feeds = [
    {
        'search'  : 'MLR team',
        'webhook' : Webhook('-- add something here --'),
        'hexcode' : '-- add something here --',
        'results' : False,
        'ping'    : True
    }, 

    {
        'search'  : 'MiLR team',
        'webhook' : Webhook(''),
        'hexcode' : '-- add something here --',
        'results' : False,
        'ping'    : True
    }
]