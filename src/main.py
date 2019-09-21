"""
A Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming soon
"""

import discord, json, os, botclass
from libs.Tools import Workers


class Cogs:
    safe = [
        "cogs.admin", "cogs.booru", "cogs.utils", "cogs.handlers",
        "cogs.roleme", "cogs.social"
    ]


with open(os.path.dirname(os.path.realpath(__file__)) +
          "/token.json") as stream:
    config_file = json.load(stream)


async def pre_fixer(bot, message):
    return await bot.cache.prefix(message)


Nolka = botclass.CachedBot(description = "A bot named Nolka",
                           config = config_file,
                           command_prefix = pre_fixer)

Nolka.remove_command("help")

for cog in Cogs.safe:
    Nolka.load_extension(cog)


@Nolka.event
async def on_ready():
    """
    Change the presence of Nolka when it is ready.
    """
    await Nolka.async_init()
    await Nolka.change_presence(activity = discord.Game(
        name = "-help for {} guilds".format(len(Nolka.guilds)), ))
    print(f"{Nolka.user.name} can chat")


@Nolka.event
async def on_guild_join(guild):
    """
    Set a flag to update the presence of Nolka and mute role scope when a guild is added
    """
    await Nolka.change_presence(activity = discord.Game(
        name = "-help for {} guilds".format(len(Nolka.guilds)), ))

    await Nolka.flag_set(guild)


@Nolka.event
async def on_guild_remove(guild):
    """
    Update the presence of Nolka when a guild is removed
    """
    await Nolka.change_presence(activity = discord.Game(
        name = "-help for {} guilds".format(len(Nolka.guilds)), ))


@Nolka.event
async def on_guild_channel_update(before, after):
    """
    Set the flag to update mute role scope when a channel is modified
    """
    await Nolka.flag_set(after.guild)


@Nolka.event
async def on_guild_channel_create(channel):
    """
    Set the flag to update mute role scope when a channel is created
    """
    await Nolka.flag_set(channel.guild)


Nolka.run(Nolka.token)
