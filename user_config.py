import praw 
from dhooks import Webhook

# Note that for this file, if there are apostrophes present fill this out BETWEEN them.

# Go to the current roster sheets. 
# For SHEET, copy/paste this part of the URL: https://docs.google.com/spreadsheets/d/ -- COPY PASTE THIS -- /edit
# For TAB, put the name of the tab that stores player names and MLR team, but replace any spaces with "%20".
# As of Session 9.9, this should be written as "Player%20List".
SHEET = '1mwwPvV8FTXpjoUC4M11ttUydyLnBl2CKbwnufrtCqy0'
TAB = 'Player%20List'

# praw = Python Reddit API Wrapper
# go to https://www.reddit.com/prefs/apps
# hit "create an app..." at the bottom
# fill in the form. hit "script" for the bubbles. fill in literally anything for the rest, it does not matter
# you will see the name of your bot, then "personal use script", then your **client_id**. copy/paste this below.
# below this (hit "edit" if it's hidden) you should see your **client_secret**. copy/paste this below.
# name user_agent literally anything; it again doesn't matter.

reddit = praw.Reddit(
    client_id     = '',
    client_secret = '',
    user_agent    = 'RSS'
)

# List of players who do *not* want to be pinged. This should be in the following format:
# ping_exclude = ['Stupido Einsteiny', 'Mark Schihne']
ping_exclude = []

# List of RSS feeds for each league. Delete those you don't need and modify those you do, while maintaining the formatting.
# To get the webhook: go to server settings, then integrations, then webhooks
# create a new webhook. name it, pick what channel you want it in, and then hit the "copy webhook URL" button and paste it below.
rss_feeds = [
    {
        'search'  : 'Oakland Athletics',    # The program looks for new comments in posts with this in the title.
        'abbrev'  : 'OAK',                  # Your team abbreviation.
        'webhook' : Webhook('https://discord.com/api/webhooks/...'),   # The webhook URL you got
        'hexcode' : '003831',               # The color of the vertical bar on the side (you choose)
        'results' : True,                   # Does your team want to see the bot's result comments, or do you have the results webhook?
        'ping'    : True,                   # Does your team want pings? You can leave this on and disable individual players above.
    }, 
    {
        'search'  : 'Golden Pride',
        'abbrev'  : 'GOP',
        'webhook' : Webhook('https://discord.com/api/webhooks/'),
        'hexcode' : '7B2C88',
        'results' : False,
        'ping'    : True,
    },
]