#!/usr/bin/python

# AOC-bot: provide scheduled C2 messages for users or groups via a discord bot
# Copyright © 2020 132nd.Professor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import asyncio
import datetime
import discord
import os
import subprocess
import sys


import config
import help
from lib import ScheduledMessage


client = discord.Client()

guild: discord.Guild
channel: discord.TextChannel

EOF = '#EOF#'

# https://discord.com/oauth2/authorize?client_id=<BOT_ID_HERE>&scope=bot&permissions=134144
@client.event
async def on_ready() -> None:
    global channel, guild
    print(f'We have logged in as {client.user}')
    print(datetime.datetime.now(tz=datetime.timezone.utc))

    # find server and channel
    for guild in client.guilds:
        if guild.name == config.GUILD:
            break
    else:
        print('Could not find server')
        sys.exit(1)

    for channel in guild.channels:
        if channel.name == config.CHANNEL:
            break
    else:
        print('Could not find channel')
        sys.exit(1)

    with open('messages.txt', 'r') as fd:
        lines = fd.readlines()
    expect_multiline_message = False  # check if we are in a multiline message
    for line in lines:
        # new message
        if not expect_multiline_message:
            datetime_str, role_name, role_mention, message_str = line.strip().split('|')
        # continuing existing message
        else:
            new_message_str = line.strip()
            message_str = message_str + '\n' + new_message_str
        # have we reached the end of the message?
        if message_str.endswith(EOF):
            expect_multiline_message = False
            message_str = message_str[:-len(EOF)]
            message = ScheduledMessage(
                datetime.datetime.fromisoformat(datetime_str),
                role_name,
                role_mention,
                message_str
            )
            await schedule_message(message)
        else:
            expect_multiline_message = True


async def schedule_message(message: ScheduledMessage) -> bool:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    # check if message is already in the past
    if message.datetime < now:
        return False
    delta = (message.datetime - now).total_seconds
    asyncio.create_task(wait_and_send_message(delta, message.message))
    return True


async def wait_and_send_message(sleep_time: int, message: str) -> None:
    global channel
    await asyncio.sleep(sleep_time)
    await channel.send(message)


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    for au in config.ALLOWED_USERS:
        if message.author.name == au[0] and message.author.discriminator == au[1]:
            break
    else:
        return

    # only react to private messages
    if message.channel.type.name not in 'private':
        return

    content = message.content
    content_lower = content.lower()

    if content_lower.startswith('help'):
        await message.channel.send(help.help_message)
        return

    if content_lower.startswith('version'):
        try:
            with open('version.txt') as fd:
                await message.channel.send('```' + fd.read() + '```')
        except FileNotFoundError:
            await message.channel.send('Could not determine version.')
        finally:
            return

    if content_lower.startswith('uptime'):
        try:
            with open('/tmp/process_timestamp.txt') as fd:
                await message.channel.send('```' + fd.read() + '```')
        except FileNotFoundError:
            await message.channel.send('Could not determine uptime.')
        finally:
            return

    datetime_str, role_str, content_str = [part.strip() for part in message.content.split('|')]
    if 'now' in datetime_str.lower():
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc) + \
                datetime.timedelta(seconds=config.IMMEDIATE_MESSAGE_OFFSET)
    else:
        if '+00:00' not in datetime_str:
            await message.channel.send(
                'The time string did not contain a timezone in the form of "+00:00". Rejecting message.'
            )
            return
        try:
            timestamp = datetime.datetime.fromisoformat(datetime_str)
        except ValueError:
            await message.channel.send('Could not parse the date and time. Please check.')
            return

    for role in guild.roles:
        if role.name == role_str:
            break
    else:
        await message.channel.send('I could not find the correct **role** for the message')
        return

    message_to_send = ScheduledMessage(timestamp, role.name, role.mention, content_str)

    # report back to the user
    await message.channel.send(
        f'At `{message_to_send.datetime}`, I will do the following: '
        f'In the server `{guild.name}`, in channel `#{channel.name}`, '
        f'I will ping the role `@{message_to_send.role_name}` with the following message:')
    await message.channel.send(f'>>> {message_to_send.content}')

    # schedule the message
    # noinspection PyBroadException
    if not await schedule_message(message_to_send):
        await message.channel.send('Could **not** schedule the message. '
                                   'Verify that the timestamp is not in the past.')
        return
    await message.channel.send('Message scheduled.')

    # save the message
    try:
        with open('messages.txt', 'a') as fd:
            fd.write(f'{message_to_send.datetime}|{role.name}|{role.mention}|{content_str}{EOF}\n')
    except IOError:
        await message.channel.send('Could **not** save the message.')
        return
    await message.channel.send('Message saved.')


if __name__ == '__main__':
    with open('/tmp/process_timestamp.txt', 'w') as ft:
        subprocess.call(['date'], stdout=ft)
    client.run(os.environ['TOKEN'])
