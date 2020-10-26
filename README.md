# AOC-bot

provide scheduled C2 messages for users or groups via a discord bot

## Usage

1. Set `messages.txt` group owership to group `nobody`, and set the group-writable permission.
2. Put discord bot token in `environment.txt`.
3. Server name (discord-API calls this `guild`) and channel name are to be configured in `config.py`.
4. Build the image with `docker-compose`. Optional: add `--build-arg GIT_HASH=$(git rev-parse --short HEAD)` to the command line. This allows to ask the bot for its version.
5. Deploy with `docker-compose`.

## misc.

AOC stands for Air Operations Center.
