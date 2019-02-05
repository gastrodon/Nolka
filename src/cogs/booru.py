"""
Booru query for a bot named Nolka
"""

from libs import Macro, BooruAPI
from discord.ext import commands

class Booru:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def gel(self, ctx, *args):
        """
        Search [gelbooru](https://gelbooru.com/) for images. Any request in a sfw channel will have `safe` appended.
        `-gel [tags]`
        """

        loading_message = "Searching..."
        if not ctx.channel.is_nsfw():
            args = (*args, "rating:safe")
            loading_message = "Searching sfw..."

        message = await ctx.send(
            embed = await Macro.send(loading_message)
        )
        try:
            response = BooruAPI.Gel(ctx, message, tags = args)
        except ZeroDivisionError:
            return await message.edit(
                embed = await Macro.send("No posts were found")
            )
        await response.start()

    @commands.command(pass_context = True)
    async def derpi(self, ctx, *args):
        """
        Search [derpibooru](https://derpibooru.org/) for images. Any request in a sfw channel will have `safe` appended. Any empty query will have `pony` appended, as empty queries don't return any data from the derpibooru api.
        """
        loading_message = "Searching..."

        if not(len(args)):
            args = ("pony",)

        if not ctx.channel.is_nsfw():
            args = (*args, "safe")
            loading_message = "searching sfw..."

        message = await ctx.send(
            embed = await Macro.send(loading_message)
        )
        try:
            response = BooruAPI.Derpi(ctx, message, tags = args)
        except ZeroDivisionError:
            return await message.edit(
                embed = await Macro.send("No posts were found")
            )
        await response.start()

    @commands.command(pass_context = True, aliases = ["e6"])
    async def e621(self, ctx, *args):
        """
        Search [e621](https://621.net/) for images. Any request in a sfw channel will have `safe` appended.
        """
        loading_message = "Searching..."

        if not ctx.channel.is_nsfw():
            args = (*args, "rating:safe")
            loading_message = "searching sfw..."

        message = await ctx.send(
            embed = await Macro.send(loading_message)
        )
        try:
            response = BooruAPI.E621(ctx, message, tags = args)
        except ZeroDivisionError:
            return await message.edit(
                embed = await Macro.send("No posts were found")
            )
        await response.start()


def setup(bot):
    bot.add_cog(Booru(bot))
