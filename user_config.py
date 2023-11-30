import praw 
from dhooks import Webhook

# praw = Python Reddit API Wrapper
# go to https://www.reddit.com/prefs/apps
# finish this description

reddit = praw.Reddit(
    client_id     = '-- insert thing here --',
    client_secret = '-- insert thing here --',
    user_agent    = '-- insert thing here --'
)

# List of players who do *not* want to be pinged. This should be in the following format:
# ping_exclude = ['Stupido Einsteiny', 'Mark Schihne']
ping_exclude = []

# List of RSS feeds for each league. Delete those you don't need and modify those you do, while maintaining the formatting.
rss_feeds = [
    {
        'search'  : 'MLR Team',
        'abbrev'  : '-- insert thing here --',
        'webhook' : Webhook('-- insert thing here --'),
        'hexcode' : '-- insert thing here --',
        'results' : False,
        'ping'    : True
    }, 

    {
        'search'  : 'MiLR Team',
        'abbrev'  : '-- insert thing here --',
        'webhook' : Webhook('-- insert thing here --'),
        'hexcode' : '-- insert thing here --',
        'results' : False,
        'ping'    : True
    }
]