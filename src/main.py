"""
A Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming soon
"""

import discord, json, os, datetime, sys, traceback
from enum import Enum
from discord.ext import commands

class Cogs:
    safe = [
        "cogs.admin",
        "cogs.booru"
    ]
    unstable = [
        "cogs.update"
    ]

with open(os.path.dirname(os.path.realpath(__file__))+"/token.json") as stream:
    token = json.load(stream)["token"]

Nolka = commands.Bot(
    command_prefix = "-",
    description = "A bot named Nolka"
)

for cog in Cogs.safe:
    try:
        Nolka.load_extension(cog)
    #TODO: Post to an error log hosted somewhere
    #https://github.com/basswaver/Nolka/issues/4
    except:
        print(f"There was an issue loading {cog}")
if "--unstable" in sys.argv:
    for cog in Cogs.unstable:
        try:
            Nolka.load_extension(cog)
        except:
            print(f"There was an issue loading unstable {cog}")
            traceback.print_exc()

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
