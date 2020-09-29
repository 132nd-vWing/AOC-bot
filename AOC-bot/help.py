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

import config

help_message = f""" To schedule a message for the server {config.GUILD}, send me a PM that looks like this:

```
<date and time> | <role> | <message>
```

- `<date and time>`: *Must* be ISO formatted, and contain date, time and timezone (see example). Currently, only UTC is supported. 
- `<role>`: This role must exist on the server. When the message is delivered, the role will be pinged.
- `<message>`: This message will be forwarded *as is* to the channel `{config.CHANNEL}`, and therefore supports all of discord's formatting options.

The individual items *must* be separated using the pipe symbol.

When I have received your message, I will report back with how the message will look like, when it is saved to disk, and when it is scheduled.

Scheduled messages can't be removed at this time. Triple-check the messages before submitting them to me.

Example:
```
2020-09-28 18:30+00:00 | Bot admin | This is a super-important message that warrants pinging some guys at a certain time.
```
"""
