import discord
from enum import Enum
from discord.ext import commands

def admin(ctx):
    """
    Return bool representing a context owner having admin rights on a server.
    """
    return ctx.message.author.permissions_in(ctx.channel).administrator

class Embed:
    @staticmethod
    async def message(description, **kwargs):
        """
        Macro for normal messages

        description: string - message text
        """
        return discord.Embed(
            type = "rich",
            description = description,
            color = kwargs.get("color", discord.Color(0x82b1ff)),
        )

    @classmethod
    async def error(cls, description, **kwargs):
        """
        Macro for error messages

        description: string - message text
        """
        return await cls.message(description, color = discord.Color(0xff72bb))

    @classmethod
    async def infraction(cls, description, **kwargs):
        """
        Macro for infraction messages

        description: string - message text
        """
        return await cls.message(description, color = discord.Color(0xffee75))

    @classmethod
    async def report(cls, description, **kwargs):
        """
        Macro for error reporting to my _special guild_

        description: string - message text
        """
        return await cls.message(description, color = discord.Color(0xbfbfbf))

    @classmethod
    async def image(cls, url, description = None, **kwargs):
        """
        Macro for images for Nolka to send

        url: string - url to the image to embed
        description: string - message text
        """
        message = await cls.message(description, **kwargs)
        message.set_image(url = url)
        return message

    @classmethod
    async def help(cls, title, helpitems, **kwargs):
        """
        Macro for a help message for Nolka to send

        title: string - title of the message
        helpitems: tuple - command-docstring pairs
        """
        message = discord.Embed(
            type = "rich",
            title = title,
            color = kwargs.get("color", discord.Color(0x82b1ff))
        )
        for item in helpitems:
            message.add_field(
                name = item[0],
                value = item[1],
                inline = False
            )
        return message

send = Embed.message
error = Embed.error
image = Embed.image
report = Embed.report
infraction = Embed.infraction
