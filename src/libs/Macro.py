import discord
from enum import Enum
from discord.ext import commands

def admin(ctx):
    """
    Return bool representing a context owner having admin rights on a server.
    """
    return ctx.message.author.permissions_in(ctx.channel).administrator

class Color():
    message = discord.Color(0x82b1ff)
    error = discord.Color(0xff72bb)

class Embed:
    @staticmethod
    async def message(description, **kwargs):
        """
        Macro for normal messages for Nolka to send

        description: string - message text
        """
        return discord.Embed(
            type = "rich",
            description = description,
            color = kwargs.get("color", Color.message),
        )

    @classmethod
    async def error(cls, description, **kwargs):
        """
        Macro for error messages for Nolka to send

        description: string - message text
        """
        return await cls.message(description, color = Color.error)

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
