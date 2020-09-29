# AOC-bot

provide scheduled C2 messages for users or groups via a discord bot

## Usage

Put discord token in `environment.txt`, and deploy with `docker-compose`. Server name (discord-API calls this `guild`) and channel name are currently hardcoded.

## Caveats

All scheduled messages are saved in `messages.txt`, which allows the bot to be restarted. Unfortunately, this only works single line messages at this time. Multi line messages in `messages.txt` will cause errors on startup.
