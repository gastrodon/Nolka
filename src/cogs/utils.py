"""
Utility commands for a bot named Nolka
"""

from libs import Macro, Messages
from discord.ext import commands

class Utils:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def ping(self, ctx, count = 1):
        """
        Return the bot's latency
        """
        try:
            int(count)
        except ValueError:
            count = 1
        for _ in range(int(count)):
            await ctx.channel.send(
                embed = await Macro.Embed.message(Messages.pingms.format(self.bot.latency * 1000))
            )

    @commands.command(pass_context = True)
    async def help(self, ctx, *args):
        if len(args) is 0:
            await ctx.channel.send()


def setup(bot):
    bot.add_cog(Utils(bot))
