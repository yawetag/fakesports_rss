# MLR RSS
This code replaces the MLR OOTC's Play by Play script currently hosted at https://github.com/MLROOTC/MLR-OOTC/tree/main/Python%20Scripts/Play%20by%20Play . This update includes the following:
- multiple MLR and MiLR team feeds through the same file instance
- pinging of users when their at-bat is posted
- ignoring of the bot's results posts

All of the above are optional changes, and the feed can be set to operate just like the OOTC's current version.

Future upgrades will include:
- low-timer notifications to both the batter and GMs
- pitcher notification
- ability to be used for other leagues

## Quick Setup Guide
To get started, complete the following steps:

### Save files
Save all of the files into a directory on the computer you want to host the bot.

### Edit config file
Open `user_config.py` and update the settings as instructed. The bot is able to run unlimited teams through this user_config, as long as each team is configured.

### Run the file
Run `python main.py` (or `python3 main.py` on some builds). If all goes well, you should see no errors on the screen. If no errors appear, the bot is running and will check reddit every 15 seconds for new posts.

If any errors appear while running, you'll need to investigate the reason why. Most of the time, it's due to improper information being stored in the user_config file. If you still cannot figure it out, you can get help through the following:
* GitHub: Enter a new issue at https://github.com/yawetag/mlr_rss/issues and it will be investigated.
* Let Stupido Einsteiny or Mark Schihne know through DMs on Discord and they will investigate.

# Requirements
The following Python libraries are required to run the MLR RSS bot. If you ever receive an error that the library isn't present, consult documentation on how to install libraries for your build:
* datetime
* dhooks
* discord
* pandas
* praw
* re
* requests
* time