import discord, sys, traceback
from libs import Macro, Messages
from discord.ext import commands

class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.get_guild(520793550624129025)

    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        ignored = (commands.CommandNotFound, commands.UserInputError)

        if isinstance(error, ignored):
            pass

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.MissingRequiredArgument)
            )
            return

        if isinstance(error, commands.BadArgument):
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.BadArgument)
            )
            return

        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.MissingPermissions)
            )
            return

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
