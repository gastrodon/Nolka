"""
Dynamic cogs for a bot named Nolka
"""

import traceback
from libs import Macro, Messages
from discord.ext import commands

class Update:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True, aliases = ["extension", "package"])
    @commands.check(Macro.snakeEater)
    async def cog(self, ctx):
        """
        Group for loading, unloading, and modifying command groups
        """
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.noSubcommand)
            )

    @cog.command(pass_context = True, aliases = ["add"])
    @commands.check(Macro.snakeEater)
    async def load(self, ctx, *args):
        """
        Load cogs for Nolka to use if they exist
        Takes a list of cogs, and requires at least one cog
        """
        if len(args) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.missingArgs)
            )
            return
        #TODO: use a generator to do this in one statement
        success = []
        failure = []
        for cog in args:
            try:
                self.bot.load_extension(cog)
                success.append(cog)
            except:
                failure.append(cog)
                traceback.print_exc()
        if success:
            await ctx.channel.send(
                embed = await Macro.Embed.message(Messages.cogsLoaded.format(", ".join(success)))
            )
        if failure:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.cogsNotLoaded.format(", ".join(failure)))
            )

    @cog.command(pass_context = True)
    @commands.check(Macro.snakeEater)
    async def unload(self, ctx, *args):
        """
        Unload cogs for Nolka to use if they are loaded
        Takes a lsit of cogs, and requires at least one loaded cog
        """
        if len(args) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.missingArgs)
            )
            return
        #TODO: use a generator here too
        success = []
        failure = []
        #TODO: check for nonexistent cogs
        for cog in args:
            try:
                self.bot.unload_extension(cog)
                success.append(cog)
            except:
                failure.append(cog)
        if success:
            await ctx.channel.send(
                embed = await Macro.Embed.message(Messages.cogsUnloaded.format(", ".join(success)))
            )
        if failure:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.cogsNotUnloaded.format(", ".join(failure)))
            )

def setup(bot):
    bot.add_cog(Update(bot))
