import discord
import praw
from dhooks import Webhook
import datetime
import time
import re

# Dict of dicts of the different RSS feeds.
#   search : The word or phrase to search in the title.
#   webhook : The webhook for the server.
#   hexcode : The hexcode for the embed border.
#   results : Whether to show the results from the subreddit. True = show results; False = don't show results
#   ping : Whether to ping the users. True = ping users; False = don't ping users
#   users : Dict of users to ping if ping = True
rss_feeds = [
    {
        "search"  : "--SEARCH_TEXT--",
        "webhook" : Webhook("--WEBHOOK--"),
        "hexcode" : "002B73",
        "results" : False,
        "ping"    : True,
        "users"   : {
            "--PLAYER NAME--"          : {"notify" : True,  "mention" : "<@--SNOWFLAKE_ID-->"},
            "--PLAYER NAME--"          : {"notify" : True,  "mention" : "<@--SNOWFLAKE_ID-->"},
        }
    },
]

#  To generate a client ID and secret, go here: https://www.reddit.com/prefs/apps scroll all the way to the bottom, and
#  hit the create an app button. Enter something for name and redirect URL, and make sure the script radio button is
#  selected. Hit the create app button, and then paste the client ID and secret below. The user_agent string literally 
#  just needs to have some text in it, does not matter what. 
reddit = praw.Reddit(
    client_id='--CLIENT_ID--',
    client_secret='--CLIENT_SECRET--',
    user_agent='--USER_AGENT--'
)

def parse_comments():
    for comment in reddit.subreddit('fakebaseball').stream.comments(skip_existing=True):
        # Go through each item in rss_feeds and see if the comment belongs
        for r in rss_feeds:
            if r['search'].lower() in comment.link_title.lower():
                # If the feed doesn't want the results post from reddit (with the flavor text), skip it
                if not r['results'] and comment.author == "FakeBaseball_Umpire" and "Pitch:" in comment.body and "Swing:" in comment.body and "Diff:" in comment.body:
                    continue

                # Otherwise, send it in an embed
                embed = discord.Embed(title=comment.link_title, url=comment.link_url, description=comment.body, color=discord.Color(value=int(r['hexcode'], 16)))
                embed.set_author(name=comment.author, url=f'https://www.reddit.com/user/{comment.author}/', icon_url='https://cdn.discordapp.com/attachments/734950735418228756/911121370207911957/reddit.png')
                embed.set_thumbnail(url=comment.author.icon_img)
                embed.set_footer(text=f'Comment posted to r/{comment.subreddit} at {datetime.datetime.fromtimestamp(comment.created_utc)} Eastern')
                image_urls = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|jpeg|gif|mp4)', comment.body)

                if len(image_urls) > 0:
                    embed.set_image(url=image_urls[0])
                
                # If the feed wants to ping the current batter, do so
                if r['ping']:
                    txt = comment.body
                    curr_batter = txt[txt.find("[")+1:txt.find("](/u/")]

                    try:    # If curr_batter matches any of the users, notify of them of the at-bat
                        if r['users'][curr_batter]['notify']:   # If user wants to be pinged, make it a mention
                            atbat_text = f"{r['users'][curr_batter]['mention']} : "
                        else:                                   # If not, just post the batter's name
                            atbat_text = f"{curr_batter} : "
                        atbat_text += f"You are up! Your timer ends <t:{int(comment.created_utc + (12 * 60 * 60))}:R> (<t:{int(comment.created_utc + (12 * 60 * 60))}:F> in your local time)."
                    except: # If curr_batter doesn't match any of the users, just leave it blank
                        atbat_text = ""
                else:   # If the team doesn't want to show at-bat text, just leave it blank
                    atbat_text = ""

                # Send the webhook
                r['webhook'].send(atbat_text, embed=embed)

while True:
    print(f"{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')} Reddit post watcher starting with the following searches:")
    for r in rss_feeds:
        print(f"     * {r['search']} -- results: {r['results']}  ping: {r['ping']}")
    try:
        parse_comments()
    except Exception as e:
        print(e)
        time.sleep(15)
    else:
        time.sleep(15)
