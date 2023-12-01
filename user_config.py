import praw 
from dhooks import Webhook

SHEET = '1mwwPvV8FTXpjoUC4M11ttUydyLnBl2CKbwnufrtCqy0'

TAB = 'Player%20List'

# praw = Python Reddit API Wrapper
# go to https://www.reddit.com/prefs/apps
# finish this description

reddit = praw.Reddit(
    client_id     = '',
    client_secret = '',
    user_agent    = ''
)

# List of players who do *not* want to be pinged. This should be in the following format:
# ping_exclude = ['Stupido Einsteiny', 'Mark Schihne']
ping_exclude = []

# List of RSS feeds for each league. Delete those you don't need and modify those you do, while maintaining the formatting.
rss_feeds = [
    {
        'search'  : '',
        'abbrev'  : '',
        'webhook' : Webhook(''),
        'hexcode' : '',
        'results' : True,
        'ping'    : True
    }, 

    {
        'search'  : '',
        'abbrev'  : '',
        'webhook' : Webhook(''),
        'hexcode' : '',
        'results' : False,
        'ping'    : True
    }
]