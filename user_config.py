import asyncpraw
from dhooks import Webhook

# Note that for this file, if there are apostrophes present fill this out BETWEEN them.

# MLR ONLY: go to the current roster sheets. 
# For SHEET, copy/paste this part of the URL: https://docs.google.com/spreadsheets/d/ -- COPY PASTE THIS -- /edit
# For TAB, put the name of the tab that stores player names and MLR team, but replace any spaces with "%20".
# As of Session 9.13, this should be written as "Player%20List".
SHEET = '1mwwPvV8FTXpjoUC4M11ttUydyLnBl2CKbwnufrtCqy0'
TAB = 'Player%20List'

# asyncpraw = Asynchronous Python Reddit API Wrapper
# go to https://www.reddit.com/prefs/apps
# hit "create an app..." at the bottom
# fill in the form. hit "script" for the bubbles. fill in literally anything for the rest, it does not matter
# you will see the name of your bot, then "personal use script", then your **client_id**. copy/paste this below.
# below this (hit "edit" if it's hidden) you should see your **client_secret**. copy/paste this below.
# name user_agent literally anything; it again doesn't matter.

async def setup_reddit():
    reddit = asyncpraw.Reddit(
        client_id     = '',
        client_secret = '',
        user_agent    = 'RSS'
    )
    
    return reddit

# List of players who do *not* want to be pinged. This should be in the following format:
# ping_exclude = ['Stupido Einsteiny', 'Mark Schihne']
ping_exclude = []

# how many hours before the end of the timer would you like to be notified?
before_end = 4

# List of RSS feeds for each league. Delete those you don't need and modify those you do, while maintaining the formatting.
# To get the webhook: go to server settings, then integrations, then webhooks
# create a new webhook. name it, pick what channel you want it in, and then hit the "copy webhook URL" button and paste it below.
rss_feeds = [
    {
        'search'  : 'Oakland Athletics', # The program looks for new comments in posts with this in the title.
        'abbrev'  : 'OAK', # Your team abbreviation.
        'webhook' : Webhook('https://discord.com/api/webhooks/...'),
        'hexcode' : '003831', # The color of the vertical bar on the side (you choose)
        'results' : True, # True: you want to see the bot's result comments (in addition to the MLR webhook), False: you do not
        'ping'    : True, # True: your team wants pings (they can be disabled at the individual level). False: nobody wants pings
        'timer'   : {'need ping' : False, 'snowflake' : None, 'end' : None}, # NO TOUCHY TOUCHY
        'leaders' : ['Six', 'Teddy Bigstick', 'Mark Schihne'] # in addition to the hitter, who is pinged when timer runs low
    }, 
    {
        'search'  : 'Golden Pride',
        'abbrev'  : 'GOP',
        'webhook' : Webhook('https://discord.com/api/webhooks/...'),
        'hexcode' : '7B2C88',
        'results' : False,
        'ping'    : True,
        'timer'   : {'need ping' : False, 'snowflake' : None, 'end' : None},
        'leaders' : ['Mark Schihne', 'Guillermo Griffey III', 'Stupido Einsteiny', 'Joe Pidgeon']
    },
        {
        'search'  : 'Kitties',
        'abbrev'  : 'KC',
        'webhook' : Webhook('https://discord.com/api/webhooks/...'),
        'hexcode' : 'F7547E',
        'ping'    : True,
        'timer'   : {'need ping' : False, 'snowflake' : None, 'end' : None},
        'leaders' : ['peaches', 'Dayman Nightman', 'Leopold Pollersbeck', 'Noodle Arm Big Power ODoyle'],
        'users'   : {
            'Dayman Nightman'             : {'notify' : True, 'mention' : '347206793824436235'}, # MLN doesn't have a nice list of discord IDs, so you have to do this manually. 
            'Dave Steib'                  : {'notify' : True, 'mention' : '397500246755901451'}, # Name, whether this user wants reminder pings, and their snowflake.
            'Fatts Richard'               : {'notify' : True, 'mention' : '757379787340906587'}, # To get the snowflake: enable developer mode in Discord settings, long press/right click them, "Copy User ID".
            'Borg Torbjorgsson'           : {'notify' : True, 'mention' : '246488195682795521'},
            'Dutch Boggs'                 : {'notify' : True, 'mention' : '166930309583994880'},
            'Alexander West'              : {'notify' : True, 'mention' : '384195152727506944'},
            'KC Bats'                     : {'notify' : True, 'mention' : '322186326130556940'},
            'Kenny Powers'                : {'notify' : True, 'mention' : '277907298112765952'},
            'Antwan Zella'                : {'notify' : True, 'mention' : '135821931550081024'},
            'Noodle Arm Big Power ODoyle' : {'notify' : True, 'mention' : '566239287713202187'},
            'peaches'                     : {'notify' : True, 'mention' : '157986981882757121'},
            'Leopold Pollersbeck'         : {'notify' : True, 'mention' : '147134307440394241'},
            'Virgil Aegis-Gunther'        : {'notify' : True, 'mention' : '1149354651825737891'},
            'Saul Pewald'                 : {'notify' : True, 'mention' : '419525278356733963'},
            'Kancing Mutlak'              : {'notify' : True, 'mention' : '362064637509763085'},
            'Brent Chillwater'            : {'notify' : True, 'mention' : '170720826557988865'},
            'Penguino'                    : {'notify' : True, 'mention' : '667860394248765450'}
        }
    }
]