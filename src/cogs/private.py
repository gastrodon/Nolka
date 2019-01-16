"""
Private message commands for a bot named Nolka
"""

from libs import Macro, Messages
from discord.ext import commands
from os import path
from json import load

class Private:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def invite(self, ctx, *args):
        """
        Return an OAuth link to add this bot to a server
        """
        with open(path.dirname(path.realpath(__file__))+"/../token.json") as stream:
            invite = load(stream)["invite"]
        await ctx.channel.send(
            embed = await Macro.Embed.message(
                Messages.inviteMessage.format(invite)
            )
        )

def setup(bot):
    bot.add_cog(Private(bot))
