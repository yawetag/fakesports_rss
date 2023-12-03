import datetime
import time
from user_config import *
from leagues import fakebaseball as mlr

LEAGUES = ['fakebaseball']

##### fakebaseball Data #######################################################
mlr_snowflakes = mlr.mlr_discord()
mlr_players = mlr.mlr_players()
milr_players = mlr.milr_players()
###############################################################################

while True:
    print(f"{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')} Reddit post watcher starting with the following searches:")

    for r in rss_feeds:
        print(f"     * {r['search']} ({r['abbrev']} - {r['subreddit']}) -- results: {r['results']} -- ping: {r['ping']}")

    try:
        mlr.parse_comments(mlr_snowflakes, mlr_players, milr_players)
    except Exception as e:
        print(e)
        time.sleep(15)
    else:
        time.sleep(15)