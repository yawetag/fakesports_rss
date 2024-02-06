import asyncio
from datetime import datetime
from parse_comments import *

async def main():
    data_setup()

    print(f"{datetime.now().strftime('%m/%d/%Y %H:%M:%S')} Reddit post watcher starting with the following searches:")

    for r in rss_feeds:
        print(f"     * {r['search']} -- ping: {r['ping']}")

    while True:
        try:
            await asyncio.gather(parse_comments(), check_timers())
        except Exception as e:
            print(e)
            await asyncio.sleep(15)
        else:
            await asyncio.sleep(15)

asyncio.run(main())