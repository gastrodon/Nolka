"""
A Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming soon
"""

import discord, json, os, botclass

class Cogs:
    safe = [
        "cogs.admin",
        "cogs.booru",
        "cogs.utils",
        "cogs.handlers",
        "cogs.roleme"
    ]


with open(os.path.dirname(os.path.realpath(__file__)) + "/token.json") as stream:
    config_file = json.load(stream)

async def pre_fixer(bot, message):
    return bot.cache[str(message.guild.id)].get("prefix", ["-"])

Nolka = botclass.CachedBot(
    description = "A bot named Nolka",
    config = config_file,
    command_prefix = pre_fixer
)

Nolka.remove_command("help")

for cog in Cogs.safe:
    #TODO: Try with a traceback
    Nolka.load_extension(cog)

@Nolka.event
async def on_ready():
    """
    Change the presence of Nolka when it is ready.
    """
    await Nolka.async_init()
    await Nolka.change_presence(activity = discord.Game(
        name = "on {} servers".format(len(Nolka.guilds)),
    ))
    print(Nolka.cache)

Nolka.run(Nolka.token)
