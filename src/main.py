"""
A Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming soon
"""

import discord, json, os, datetime
from enum import Enum
from discord.ext import commands

class Cogs:
    safe = [
        "cogs.admin",
        "cogs.booru"
    ]

with open(os.path.dirname(os.path.realpath(__file__))+"/token.json") as stream:
    token = json.load(stream)["token"]

Nolka = commands.Bot(
    command_prefix = "-",
    description = "A bot named Nolka"
)

for cog in Cogs.safe:
    Nolka.load_extension(cog)

#TODO: I have no idea how the presence is supposed to work
@Nolka.event
async def on_ready():
    """
    Change the presence of Nolka when it is ready.
    """
    ftime = [
        datetime.datetime.now().strftime("%B"),
        datetime.datetime.now().strftime("%d"),
        datetime.datetime.now().strftime("%Y")
    ]
    await Nolka.change_presence(activity = discord.Game(
        name = datetime.datetime.now().strftime("Online since %{} %{}th %{}".format(*ftime)),
        type = 1,
        description = "desc"
    ))

Nolka.run(token)
