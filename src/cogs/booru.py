"""
Booru query for a bot named Nolka
"""

from libs import Macro, BooruAPI, Messages
from libs.Tools import BooruNoPosts
from discord.ext import commands

class Booru:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def gel(self, ctx, *args):
        message = await ctx.send(
            embed = await Macro.send(Messages.booruSearching)
        )
        response = BooruAPI.Gel(ctx, message, tags = args)
        await response.start()

def setup(bot):
    bot.add_cog(Booru(bot))
