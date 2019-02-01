"""
Booru query for a bot named Nolka
"""

from libs import Macro, BooruAPI
from libs.Tools import BooruNoPosts
from discord.ext import commands

class Booru:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def gel(self, ctx, *args):
        """
        Search [gelbooru](https://gelbooru.com/) for images. If called in a sfw channel, any request will have `-rating:explicit` appended
        `-gel [tags]`
        """

        loading_message = "Searching..."
        if not ctx.channel.is_nsfw():
            args = (*args, "-rating:explicit")
            loading_message = "Searching sfw..."

        message = await ctx.send(
            embed = await Macro.send(loading_message)
        )

        response = BooruAPI.Gel(ctx, message, tags = args)
        await response.start()

def setup(bot):
    bot.add_cog(Booru(bot))
