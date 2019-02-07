from libs import Macro
from discord.ext import commands

class Voice:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def play(self, ctx):
        """
        Play
        """

def setup(bot):
    bot.add_cog(Voice(bot))
