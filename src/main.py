"""
A Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming soon
"""

import discord, json, os, datetime, sys, traceback
from discord.ext import commands

class Cogs:
    safe = [
        "cogs.admin",
        "cogs.booru",
        "cogs.update",
        "cogs.utils",
        "cogs.handlers"
    ]
    unstable = [
    ]

with open(os.path.dirname(os.path.realpath(__file__)) + "/token.json") as stream:
    token = json.load(stream)["token"]

Nolka = commands.Bot(
    command_prefix = "-",
    description = "A bot named Nolka"
)

Nolka.remove_command("help")

for cog in Cogs.safe:
    #TODO: Try with a traceback
    Nolka.load_extension(cog)

#TODO: I have no idea how the presence is supposed to work
@Nolka.event
async def on_ready():
    """
    Change the presence of Nolka when it is ready.
    """
    await Nolka.change_presence(activity = discord.Game(
        name = datetime.datetime.now().strftime("with cogs"),
        type = 1,
        description = "Hello, world!"
    ))

Nolka.run(token)
