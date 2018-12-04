"""
Utility commands for a bot named Nolka
"""

from libs import Macro, Messages
from discord.ext import commands

class Utils:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def ping(self, ctx):
        """
        Return the bot's latency
        """
        await ctx.channel.send(
            embed = await Macro.Embed.message(str(self.bot.latency))
        )

def setup(bot):
    bot.add_cog(Utils(bot))
