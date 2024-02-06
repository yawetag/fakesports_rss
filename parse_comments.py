import discord
import requests
import re
import pandas as pd
import asyncio
import pytz
from datetime import datetime, timedelta
from user_config import *

snowflakes = None
mlr = None
milr = None

def data_setup():
    global snowflakes, mlr, milr
    url = 'https://www.rslashfakebaseball.com/api/players'
    response = requests.get(url)
    raw_data = response.json()
    snowflakes = {item['playerName']:item['discordID'] for item in raw_data}
    
    for r in rss_feeds:
        if 'users' in r:
            for name in r['users']:
                snowflakes[name] = r['users'][name]['mention']

    mlr = {item['playerName']:item['Team'] for item in raw_data}
    url = f'https://docs.google.com/spreadsheets/d/{SHEET}/gviz/tq?tqx=out:csv&sheet={TAB}'
    milr = pd.read_csv(url)
    milr = milr[['Name', 'MiLR Team']]
    milr = milr.set_index('Name').to_dict()['MiLR Team']

async def parse_comments():
    reddit = await setup_reddit()
    subreddit = await reddit.subreddit('fakebaseball+baseballbythenumbers')
    async for comment in subreddit.stream.comments(skip_existing = True):
        if comment.subreddit == 'fakebaseball':
            await mlr_parse(comment)
        elif comment.subreddit == 'baseballbythenumbers':
            await mln_parse(comment)

async def check():
    global rss_feeds
    print(f'Checking timers... ({datetime.utcnow()})')

    for r in rss_feeds:
        if r['timer']['need ping'] == True and r['timer']['end'] - datetime.utcnow() < timedelta(hours = before_end):
            text_to_send = f"<@{r['timer']['snowflake']}> has less than {before_end} hours left!"
            
            for leader in r['leaders']:
                text_to_send += f' <@{snowflakes[leader]}>'

            r['webhook'].send(text_to_send)
            r['timer']['need ping'] = False

async def check_timers():
    while True:
        await check()
        await asyncio.sleep(60)

async def mlr_parse(comment):
    # Go through each of the rss_feeds and see if the comment belongs
    for r in rss_feeds:
        if r['search'].lower() in comment.link_title.lower():
            await comment.author.load()
            utc_timestamp = datetime.utcfromtimestamp(comment.created_utc)
            est = pytz.timezone('US/Eastern')
            est_timestamp = utc_timestamp.replace(tzinfo=pytz.utc).astimezone(est)

            # If that particular team does not want the results post with the flavor text, skip it
            if not r['results'] and comment.author == 'FakeBaseball_Umpire' and 'Pitch:' in comment.body and 'Swing:' in comment.body and 'Diff:' in comment.body:
                continue

            # Otherwise, send the comment in an embed
            embed = discord.Embed(title = comment.link_title, url = comment.link_url, description = comment.body, color = discord.Color(value = int(r['hexcode'], 16)))
            embed.set_author(name = comment.author, url = f'https://www.reddit.com/user/{comment.author}/', icon_url = 'https://cdn.discordapp.com/attachments/734950735418228756/911121370207911957/reddit.png')
            embed.set_thumbnail(url = comment.author.icon_img)
            embed.set_footer(text=f'Comment posted to r/{comment.subreddit} at {est_timestamp.strftime("%Y-%m-%d %H:%M:%S")} Eastern')
            image_urls = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|jpeg|gif|mp4)', comment.body)

            if len(image_urls) > 0:
                embed.set_image(url=image_urls[0])

            # If the feed wants to ping the current batter, do so
            if r['ping']:
                txt = comment.body
                curr_batter = txt[txt.find('[')+1:txt.find('](/u/')]

                # if curr_batter matches 
                try:
                    if curr_batter not in ping_exclude and mlr[curr_batter] == r['abbrev'] or milr[curr_batter] == r['abbrev']:
                        snowflake = snowflakes[curr_batter]
                        r['timer']['snowflake'] = snowflakes[curr_batter]
                        atbat_text = f'<@{snowflake}> '
                        r['timer']['need ping'] = True
                        r['timer']['end'] = datetime.utcnow() + timedelta(hours = 12)
                    else:                                   # If not, just post the batter's name
                        atbat_text = f'{curr_batter} '

                    atbat_text += f'is up! The timer ends <t:{int(comment.created_utc + (12 * 60 * 60))}:R> (<t:{int(comment.created_utc + (12 * 60 * 60))}:F> in your local time).'
                    r['timer']['end'] = datetime.utcnow() + timedelta(hours = 12)

                # If curr_batter doesn't match any of the users, just leave it blank
                except:
                    atbat_text = ''
                    r['timer']['need ping'] = False

            # If the team doesn't want to show at-bat text, just leave it blank
            else:
                atbat_text = ''

            # Send the webhook
            r['webhook'].send(atbat_text, embed=embed)

async def mln_parse(comment):
    # Go through each of the rss_feeds and see if the comment belongs
    for r in rss_feeds:
        if r['search'].lower() in comment.link_title.lower():
            await comment.author.load()
            utc_timestamp = datetime.utcfromtimestamp(comment.created_utc)
            est = pytz.timezone('US/Eastern')
            est_timestamp = utc_timestamp.replace(tzinfo=pytz.utc).astimezone(est)

            # send the comment in an embed
            embed = discord.Embed(title = comment.link_title, url = comment.link_url, description = comment.body, color = discord.Color(value = int(r['hexcode'], 16)))
            embed.set_author(name = comment.author, url = f'https://www.reddit.com/user/{comment.author}/', icon_url = 'https://cdn.discordapp.com/attachments/734950735418228756/911121370207911957/reddit.png')
            embed.set_thumbnail(url = comment.author.icon_img)
            embed.set_footer(text=f'Comment posted to r/{comment.subreddit} at {est_timestamp.strftime("%Y-%m-%d %H:%M:%S")} Eastern')
            image_urls = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|jpeg|gif|mp4)', comment.body)

            if len(image_urls) > 0:
                embed.set_image(url=image_urls[0])

            # If the feed wants to ping the current batter, do so
            if r['ping']:
                curr_batter = ''
                atbat_text = ''
                txt = comment.body

                if '](/u/' in txt:
                    curr_batter = txt[txt.find('[')+1:txt.find('](/u/')]

                if len(curr_batter) > 0:
                    # if curr_batter matches 
                    try:
                        if curr_batter in r['users'] and r['users'][curr_batter]['notify'] == True:
                            snowflake = r['users'][curr_batter]['mention']
                            r['timer']['snowflake'] = r['users'][curr_batter]['mention']
                            r['timer']['need ping'] = True
                            atbat_text = f'<@{snowflake}> '
                        else:                                   # If not, just post the batter's name
                            atbat_text = f'{curr_batter} '

                        if 7 <= est_timestamp.hour < 14:
                            atbat_text += f'is up! The timer ends <t:{int(comment.created_utc + (10 * 60 * 60))}:R> (<t:{int(comment.created_utc + (10 * 60 * 60))}:F> in your local time).'
                            r['timer']['end'] = datetime.utcnow() + timedelta(hours = 10)
                        else:
                            atbat_text += f'is up! The timer ends <t:{int(comment.created_utc + (14 * 60 * 60))}:R> (<t:{int(comment.created_utc + (14 * 60 * 60))}:F> in your local time).'
                            r['timer']['end'] = datetime.utcnow() + timedelta(hours = 14)

                    # If curr_batter doesn't match any of the users, just leave it blank
                    except:
                        atbat_text = ''
                else:
                    r['timer']['need ping'] = False

            # If the team doesn't want to show at-bat text, just leave it blank
            else:
                atbat_text = ''

            # Send the webhook
            r['webhook'].send(atbat_text, embed=embed)