import datetime
import time
from parse_comments import *

snowflakes = get_snowflakes()

while True:
    print(f"{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')} Reddit post watcher starting with the following searches:")

    for r in rss_feeds:
        print(f"     * {r['search']} -- results: {r['results']}  ping: {r['ping']}")

    try:
        parse_comments(snowflakes)
    except Exception as e:
        print(e)
        time.sleep(15)
    else:
        time.sleep(15)