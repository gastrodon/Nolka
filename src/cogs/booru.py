"""
Booru query for a bot named Nolka
"""

from libs import Macro, BooruAPI, Messages
from libs.Tools import BooruNoPosts
from emoji import demojize, emojize
from discord.ext import commands

class Booru:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def booru(self, ctx, *args):
        message = await ctx.send(
            embed = await Macro.send(Messages.booruSearching)
        )
        response = BooruAPI.PostList(ctx, message, tags = args)
        await response.edit_message()

def setup(bot):
    bot.add_cog(Booru(bot))
