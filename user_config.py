import praw 
from dhooks import Webhook

SHEET = '1mwwPvV8FTXpjoUC4M11ttUydyLnBl2CKbwnufrtCqy0'

TAB = 'Player%20List'

# praw = Python Reddit API Wrapper
# go to https://www.reddit.com/prefs/apps
# finish this description

reddit = praw.Reddit(
    client_id     = 'FILL THIS IN',
    client_secret = 'FILL THIS IN',
    user_agent    = 'FILL THIS IN'
)

# List of players who do *not* want to be pinged. This should be in the following format:
# ping_exclude = ['Stupido Einsteiny', 'Mark Schihne']
ping_exclude = []

# List of RSS feeds for each league. Delete those you don't need and modify those you do, while maintaining the formatting.
rss_feeds = [
    {
        'search'  : 'FILL THIS IN',
        'abbrev'  : 'FILL THIS IN',
        'webhook' : Webhook('FILL THIS IN'),
        'hexcode' : 'FILL THIS IN',
        'results' : True,
        'ping'    : True
    }, 

    {
        'search'  : 'FILL THIS IN',
        'abbrev'  : 'FILL THIS IN',
        'webhook' : Webhook('FILL THIS IN'),
        'hexcode' : 'FILL THIS IN',
        'results' : False,
        'ping'    : True
    }
]